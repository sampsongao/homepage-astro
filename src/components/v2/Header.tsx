import React from 'react';

export const NAV_LINKS = [
  { name: 'Experience', href: '#experience' },
  { name: 'Projects', href: '#projects' },
  { name: 'Blog', href: '/v2/blogs' },
  { name: 'Contact', href: '#contact' },
];

export default function Header(props: { pathname: string }) {
  const handleScroll = (e: React.MouseEvent<HTMLAnchorElement>, href: string) => {
    if (href.startsWith('#')) {
      e.preventDefault();
      const element = document.getElementById(href.substring(1));
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
      }
    }
  };

  return (
    <header className="sticky top-0 z-50 w-full backdrop-blur-md bg-black/50 border-b border-white/5">
      <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
        <a href="/" className="flex items-center gap-3 group">
          <div className="w-10 h-10 border border-[#d4af37] flex items-center justify-center font-serif text-[#d4af37] text-xl font-bold group-hover:bg-[#d4af37] group-hover:text-black transition-all duration-300">
            S
          </div>
          <span className="font-medium tracking-widest text-sm uppercase hidden sm:block">Sampson Gao</span>
        </a>

        <nav className="hidden md:flex items-center gap-8">
          {NAV_LINKS.map((link) => (
            <a
              key={link.name}
              href={link.href}
              onClick={(e) => handleScroll(e, link.href)}
              className="text-zinc-400 text-xs uppercase tracking-widest hover:text-zinc-100 transition-colors"
            >
              {link.name}
            </a>
          ))}
          <button className="px-5 py-2.5 bg-white text-black text-[10px] font-bold uppercase tracking-widest hover:bg-zinc-100 transition-colors">
            Resume
          </button>
        </nav>

        {/* Mobile Menu Icon */}
        <button className="md:hidden text-white">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 8h16M4 16h16" />
          </svg>
        </button>
      </div>
    </header>
  );
};
