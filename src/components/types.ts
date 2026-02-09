
export interface ExperienceItem {
  role: string;
  company: string;
  period: string;
  description: string;
  icon?: string;
}

export interface ProjectItem {
  title: string;
  description: string;
  image: string;
  tags: string[];
  link?: string;
}

export interface StatItem {
  value: string;
  label: string;
}

export interface BlogPost {
  title: string;
  excerpt: string;
  date: string;
  readTime: string;
  category: string;
}
