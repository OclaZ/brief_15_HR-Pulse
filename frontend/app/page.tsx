"use client";

import { useState, useEffect } from "react";

// Mise à jour de l'interface pour inclure plus de détails
interface Job {
  id: number;
  job_title: string;
  skills_extracted: string;
  company_name?: string;
  location?: string;
  salary_estimate?: string;
}

export default function Dashboard() {
  const [rating, setRating] = useState<number>(3.5);
  const [skills, setSkills] = useState<string>("python, sql, machine learning");
  const [predictedSalary, setPredictedSalary] = useState<number | null>(null);
  const [loadingPredict, setLoadingPredict] = useState<boolean>(false);

  const [jobs, setJobs] = useState<Job[]>([]);
  const [searchSkill, setSearchSkill] = useState<string>("");
  const [loadingJobs, setLoadingJobs] = useState<boolean>(false);
  const [uploading, setUploading] = useState<boolean>(false);

  useEffect(() => {
    fetchJobs(searchSkill);
  }, [searchSkill]);

  const fetchJobs = async (skillFilter: string) => {
    setLoadingJobs(true);
    try {
      // On demande plus de résultats pour remplir notre nouvelle grille
      let url = `${process.env.NEXT_PUBLIC_API_URL}/jobs?limit=12`;
      if (skillFilter) url += `&skill=${skillFilter}`;
      
      const res = await fetch(url);
      if (res.ok) {
        const data = await res.json();
        setJobs(data);
      }
    } catch (error) {
      console.error("Erreur API:", error);
    } finally {
      setLoadingJobs(false);
    }
  };

  const handlePredict = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoadingPredict(true);
    try {
      const skillsArray = skills.split(",").map((s) => s.trim().toLowerCase());
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/predict-salary`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ rating, skills: skillsArray }),
      });
      if (!response.ok) throw new Error();
      const data = await response.json();
      setPredictedSalary(data.predicted_salary_k);
    } catch (error) {
      alert("Erreur de prédiction.");
    } finally {
      setLoadingPredict(false);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;
    setUploading(true);
    const formData = new FormData();
    formData.append("file", e.target.files[0]);

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/upload`, { method: "POST", body: formData });
      const data = await res.json();
      alert(data.message);
    } catch (error) {
      alert("Erreur d'upload.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <main className="min-h-screen bg-[#FAF9F6] font-sans text-[#3B4D35] selection:bg-[#5E8B7E] selection:text-white pb-16">
      
      {/* Navbar Premium */}
      <nav className="bg-white border-b border-[#E8E6D9] px-8 py-4 flex items-center justify-between sticky top-0 z-20 shadow-sm">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-[#5E8B7E] flex items-center justify-center text-white font-bold text-xl shadow-md">HP</div>
          <span className="text-2xl font-extrabold tracking-tight text-[#3B4D35]">HR-Pulse <span className="font-light text-[#5E8B7E]">AI</span></span>
        </div>
        <div className="flex items-center gap-6">
          <div className="relative">
            <svg className="w-5 h-5 absolute left-3 top-2.5 text-[#5E8B7E]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
            <input 
              type="text" 
              placeholder="Rechercher une compétence..." 
              value={searchSkill}
              onChange={(e) => setSearchSkill(e.target.value)}
              className="pl-10 pr-4 py-2 border border-[#D5D2C1] rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-[#5E8B7E] bg-[#FAF9F6] w-72 transition-all"
            />
          </div>
          <label className="cursor-pointer text-sm font-bold text-[#5E8B7E] bg-[#5E8B7E]/10 px-5 py-2.5 rounded-full hover:bg-[#5E8B7E]/20 transition-colors flex items-center gap-2">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" /></svg>
            {uploading ? "Chargement..." : "Importer CSV"}
            <input type="file" accept=".csv" className="hidden" onChange={handleFileUpload} disabled={uploading} />
          </label>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-6 mt-10 space-y-12">
        
        {/* Section IA - Format Horizontal */}
        <section className="bg-white rounded-3xl shadow-lg shadow-[#3B4D35]/5 border border-[#E8E6D9] p-8 overflow-hidden relative">
          <div className="absolute top-0 right-0 w-64 h-64 bg-[#FCE651] rounded-full blur-[100px] opacity-20 pointer-events-none"></div>
          
          <div className="mb-6">
            <h1 className="text-3xl font-black tracking-tight mb-2">Estimateur de Salaire <span className="text-[#5E8B7E]">IA</span></h1>
            <p className="text-[#55634D]">Configurez le profil recherché pour obtenir la tendance du marché.</p>
          </div>

          <form onSubmit={handlePredict} className="flex flex-col md:flex-row gap-6 items-end relative z-10">
            <div className="w-full md:w-48">
              <label className="block text-sm font-bold mb-2">Note Entreprise (1-5)</label>
              <input type="number" step="0.1" min="1" max="5" value={rating} onChange={(e) => setRating(Number(e.target.value))} className="w-full bg-[#FAF9F6] border border-[#D5D2C1] rounded-xl px-4 py-3 focus:ring-2 focus:ring-[#5E8B7E] focus:outline-none" required />
            </div>
            <div className="flex-1 w-full">
              <label className="block text-sm font-bold mb-2">Compétences exigées</label>
              <input type="text" value={skills} onChange={(e) => setSkills(e.target.value)} className="w-full bg-[#FAF9F6] border border-[#D5D2C1] rounded-xl px-4 py-3 focus:ring-2 focus:ring-[#5E8B7E] focus:outline-none" placeholder="ex: python, aws, docker..." required />
            </div>
            <button type="submit" disabled={loadingPredict} className="w-full md:w-auto bg-[#3B4D35] hover:bg-[#2A3825] text-white font-bold py-3 px-8 rounded-xl transition-all active:scale-[0.98] shadow-md whitespace-nowrap">
              {loadingPredict ? "Analyse..." : "Lancer l'IA"}
            </button>

            {/* Affichage du résultat intégré */}
            {predictedSalary !== null && (
              <div className="w-full md:w-auto bg-[#FCE651] border border-[#E5D045] rounded-xl px-6 py-2.5 flex flex-col justify-center animate-in zoom-in duration-300">
                <span className="text-[10px] font-bold uppercase tracking-wider text-[#5A5000]">Estimation</span>
                <span className="text-2xl font-black text-[#3B4D35]">${predictedSalary}k <span className="text-sm font-bold opacity-70">/an</span></span>
              </div>
            )}
          </form>
        </section>

        {/* Section Offres - Format Grille */}
        <section>
          <div className="flex justify-between items-end mb-6">
            <div>
              <h2 className="text-2xl font-black text-[#3B4D35]">Offres sur le marché</h2>
              <p className="text-[#55634D] text-sm mt-1">Données extraites et analysées via Azure AI.</p>
            </div>
            <span className="text-xs font-bold uppercase tracking-wider text-[#5E8B7E] bg-[#5E8B7E]/10 px-4 py-1.5 rounded-full">
              {jobs.length} résultats
            </span>
          </div>

          {loadingJobs ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[1, 2, 3, 4, 5, 6].map((i) => (
                <div key={i} className="bg-white h-48 rounded-2xl border border-[#E8E6D9] animate-pulse"></div>
              ))}
            </div>
          ) : jobs.length === 0 ? (
            <div className="bg-white border-2 border-dashed border-[#D5D2C1] rounded-2xl py-20 text-center">
              <p className="text-lg font-bold text-[#3B4D35]">Aucune offre trouvée.</p>
              <p className="text-[#55634D]">Essayez une autre compétence ou importez de nouvelles données.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {jobs.map((job) => {
                let parsedSkills: string[] = [];
                try { parsedSkills = JSON.parse(job.skills_extracted); } catch (e) { }

                return (
                  <div key={job.id} className="bg-white p-6 rounded-2xl border border-[#E8E6D9] hover:shadow-xl hover:shadow-[#5E8B7E]/10 hover:-translate-y-1 transition-all group flex flex-col h-full">
                    {/* En-tête de la carte */}
                    <div className="flex justify-between items-start mb-4">
                      <div className="w-12 h-12 rounded-lg bg-[#FAF9F6] border border-[#E8E6D9] flex items-center justify-center font-bold text-[#5E8B7E] text-lg group-hover:bg-[#5E8B7E] group-hover:text-white transition-colors">
                        {job.company_name ? job.company_name.substring(0, 2).toUpperCase() : "CO"}
                      </div>
                      <span className="bg-[#FAF9F6] text-[#55634D] text-xs font-bold px-3 py-1 rounded-full border border-[#E8E6D9]">
                        {job.salary_estimate || "Salaire non précisé"}
                      </span>
                    </div>

                    {/* Informations principales */}
                    <h3 className="font-bold text-xl text-[#3B4D35] capitalize mb-1 line-clamp-1">{job.job_title}</h3>
                    <div className="flex items-center gap-1.5 text-sm text-[#55634D] mb-5">
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.243-4.243a8 8 0 1111.314 0z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
                      {job.location || "Localisation inconnue"} • {job.company_name || "Entreprise confidentielle"}
                    </div>

                    {/* Compétences (Poussées vers le bas grâce au mt-auto) */}
                    <div className="mt-4 pt-4 border-t border-[#E8E6D9]">
  <p className="text-xs font-bold text-[#3B4D35] uppercase mb-3">Stack IA détectée :</p>
  <div className="flex flex-wrap gap-2">
    {parsedSkills.length > 0 ? (
      parsedSkills.map((skill, idx) => (
        <span key={idx} className="bg-[#5E8B7E]/10 text-[#5E8B7E] border border-[#5E8B7E]/20 px-2.5 py-1 rounded-md text-xs font-bold uppercase tracking-wide">
          {skill}
        </span>
      ))
    ) : (
      <span className="text-sm text-gray-400 italic">Aucune compétence isolée</span>
    )}
  </div>
</div>
                  </div>
                );
              })}
            </div>
          )}
        </section>

      </div>
    </main>
  );
}