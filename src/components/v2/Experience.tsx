import React from 'react';
import { EXPERIENCE } from './constants';

const Experience: React.FC = () => {
  return (
    <section id="experience" className="py-32 px-6">
      <div className="max-w-7xl mx-auto">
        <div className="flex flex-col justify-between mb-20 gap-8">
          <h2 className="font-serif text-4xl italic text-white">Professional Experiences</h2>
        </div>

        <div className="space-y-16">
          {EXPERIENCE.map((exp) => (
            <div key={exp.id} className="group relative grid md:grid-cols-[1fr_2fr] gap-8 pb-16 border-b border-white/5 last:border-0">
              {/* Left Column: Icon & Company */}
              <div className="flex flex-col gap-4">
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 bg-zinc-900 flex items-center justify-center border border-white/5 text-[#d4af37]">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                    </svg>
                  </div>
                  <div>
                    <h4 className="text-[#d4af37] text-[10px] font-bold uppercase tracking-widest">{exp.company}</h4>
                    <p className="text-zinc-500 text-xs font-mono">{exp.period}</p>
                  </div>
                </div>
              </div>

              {/* Right Column: Role & Description */}
              <div className="space-y-4">
                <h3 className="text-2xl font-semibold text-white group-hover:text-[#d4af37] transition-colors">{exp.role}</h3>
                <p className="text-zinc-400 leading-relaxed font-light text-lg">
                  {exp.description}
                </p>
              </div>
              
              {/* Decorative side border that glows on hover */}
              <div className="absolute top-0 left-[-20px] h-full w-[2px] bg-white/0 group-hover:bg-[#d4af37] transition-all duration-500"></div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Experience;
