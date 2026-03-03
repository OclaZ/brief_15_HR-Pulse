"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";

interface Job {
  id: number;
  job_title: string;
  skills_extracted: string;
  company_name?: string;
  location?: string;
  salary_estimate?: string;
}

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.1 }
  }
};

const itemVariants = {
  hidden: { y: 20, opacity: 0 },
  visible: { y: 0, opacity: 1 }
};

export default function Dashboard() {
  const [rating, setRating] = useState<number>(3.5);
  const [jobTitle, setJobTitle] = useState<string>("Data Scientist");
  const [locationInput, setLocationInput] = useState<string>("New York, NY");
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
        // Envoi des nouvelles données requises par le Pipeline Backend
        body: JSON.stringify({ 
          job_title: jobTitle,
          location: locationInput,
          rating, 
          skills: skillsArray 
        }),
      });
      const data = await response.json();
      setPredictedSalary(data.predicted_salary_k);
    } catch (error) {
      alert("Erreur de prédiction.");
    } finally {
      setLoadingPredict(false);
    }
  };

  return (
    <main className="min-h-screen bg-[#F8F9FA] font-sans text-[#1A1C19] pb-20">
      
      <nav className="sticky top-0 z-50 backdrop-blur-md bg-white/70 border-b border-slate-200/60 px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <motion.div initial={{ x: -20, opacity: 0 }} animate={{ x: 0, opacity: 1 }} className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#5E8B7E] to-[#2F4F4F] flex items-center justify-center text-white font-bold text-xl">H</div>
            <span className="text-2xl font-black tracking-tight text-[#3B4D35]">HR-Pulse</span>
          </motion.div>

          <div className="flex items-center gap-4">
            <input 
              type="text" 
              placeholder="Filtrer par skill..." 
              value={searchSkill}
              onChange={(e) => setSearchSkill(e.target.value)}
              className="pl-4 pr-4 py-2 bg-slate-100 rounded-xl text-sm outline-none w-64"
            />
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-6 pt-12">
        
        <motion.section initial={{ y: 30, opacity: 0 }} animate={{ y: 0, opacity: 1 }} className="bg-white rounded-[2rem] p-10 border border-slate-200 shadow-sm relative overflow-hidden">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
            <div className="lg:col-span-3">
              <h2 className="text-4xl font-black text-[#3B4D35]">Salary <span className="text-[#5E8B7E]">AI</span></h2>
              <p className="mt-2 text-slate-500 text-sm">Prédisez le salaire idéal basé sur le poste, la ville et les skills.</p>
            </div>

            <div className="lg:col-span-9 bg-slate-50 p-6 rounded-[1.5rem]">
              <form onSubmit={handlePredict} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {/* Champ Titre du Poste */}
                  <div className="space-y-1">
                    <span className="text-[10px] font-bold uppercase text-slate-400">Poste</span>
                    <input type="text" value={jobTitle} onChange={(e) => setJobTitle(e.target.value)} className="w-full bg-white rounded-xl px-4 py-3 text-sm outline-none shadow-sm" />
                  </div>
                  {/* Champ Localisation */}
                  <div className="space-y-1">
                    <span className="text-[10px] font-bold uppercase text-slate-400">Localisation</span>
                    <input type="text" value={locationInput} onChange={(e) => setLocationInput(e.target.value)} className="w-full bg-white rounded-xl px-4 py-3 text-sm outline-none shadow-sm" />
                  </div>
                  {/* Champ Note */}
                  <div className="space-y-1">
                    <span className="text-[10px] font-bold uppercase text-slate-400">Note Entreprise</span>
                    <select value={rating} onChange={(e) => setRating(Number(e.target.value))} className="w-full bg-white rounded-xl px-4 py-3 text-sm outline-none shadow-sm">
                      {[1,2,3,4,5].map(n => <option key={n} value={n}>{n}.0</option>)}
                      <option value={3.5}>3.5</option>
                    </select>
                  </div>
                </div>

                <div className="flex flex-col md:flex-row gap-4 items-end">
                  <div className="flex-1 space-y-1 w-full">
                    <span className="text-[10px] font-bold uppercase text-slate-400">Compétences</span>
                    <input type="text" value={skills} onChange={(e) => setSkills(e.target.value)} className="w-full bg-white rounded-xl px-4 py-3 text-sm outline-none shadow-sm" />
                  </div>
                  
                  <motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }} className="bg-[#3B4D35] text-white font-bold h-[48px] px-8 rounded-xl shadow-lg">
                    {loadingPredict ? "..." : "Prédire"}
                  </motion.button>

                  <AnimatePresence>
                    {predictedSalary && (
                      <motion.div initial={{ opacity: 0, x: 10 }} animate={{ opacity: 1, x: 0 }} className="bg-yellow-300 px-6 py-2 rounded-xl border-b-4 border-yellow-500 flex flex-col items-center">
                        <span className="text-[9px] font-black text-yellow-800 uppercase">Estimé</span>
                        <span className="text-lg font-black text-[#3B4D35]">${predictedSalary}k</span>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
              </form>
            </div>
          </div>
        </motion.section>

        <section className="mt-16">
          <h2 className="text-3xl font-black text-[#3B4D35] mb-8">Dernières Offres</h2>
          <motion.div variants={containerVariants} initial="hidden" animate="visible" className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {loadingJobs ? (
              <div className="col-span-full text-center py-10">Chargement...</div>
            ) : (
              jobs.map((job) => (
                <motion.div key={job.id} variants={itemVariants} whileHover={{ y: -5 }} className="bg-white p-6 rounded-[1.5rem] border border-slate-200 shadow-sm hover:shadow-md transition-all">
                  <div className="flex justify-between items-start mb-4">
                    <div className="w-12 h-12 bg-slate-50 rounded-xl flex items-center justify-center text-[#5E8B7E] font-bold border border-slate-100">{job.company_name?.charAt(0)}</div>
                    <div className="px-3 py-1 bg-[#5E8B7E]/10 text-[#5E8B7E] text-[10px] font-black rounded-full uppercase">{job.salary_estimate || "TBD"}</div>
                  </div>
                  <h3 className="text-lg font-bold text-[#3B4D35] truncate">{job.job_title}</h3>
                  <p className="text-xs text-slate-400 mt-1">{job.location} • {job.company_name}</p>
                  <div className="mt-6 pt-4 border-t border-slate-50 flex flex-wrap gap-2">
                    {JSON.parse(job.skills_extracted).slice(0, 3).map((s: string, i: number) => (
                      <span key={i} className="px-2 py-1 bg-slate-50 text-slate-500 text-[9px] font-bold rounded-lg border border-slate-100 uppercase">{s}</span>
                    ))}
                  </div>
                </motion.div>
              ))
            )}
          </motion.div>
        </section>
      </div>
    </main>
  );
}