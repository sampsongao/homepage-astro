import { ExperienceItem, ProjectItem, StatItem, BlogPost } from './types';

export const STATS: StatItem[] = [
  { value: '8+', label: 'Years of Engineering' },
  { value: '250M+', label: 'API Requests Handled' },
  { value: '42', label: 'Open Source Contribs' },
];

export const EXPERIENCE: ExperienceItem[] = [
  {
    id: '1',
    role: 'Senior Software Engineer',
    company: 'Quantum Systems Group',
    period: '2021 — Present',
    description: 'Leading the development of high-throughput distributed architectures. Focused on scalability and low-latency microservices using Go and Rust.',
  },
  {
    id: '2',
    role: 'Full Stack Engineer',
    company: 'Aetheric Networks',
    period: '2018 — 2021',
    description: 'Designed and implemented end-to-end cloud solutions for telecommunications. Spearheaded the migration of legacy monoliths to AWS Lambda and serverless frameworks.',
  },
  {
    id: '3',
    role: 'Software Developer',
    company: 'Silicon Dynamics',
    period: '2016 — 2018',
    description: 'Developed internal tooling for chip performance analysis. Optimized Python data pipelines resulting in a 40% reduction in processing time.',
  },
];

export const BLOG_POSTS: BlogPost[] = [
  {
    id: '1',
    title: 'The Future of Distributed Systems',
    excerpt: 'Exploring the transition from centralized clouds to decentralized edge computing networks.',
    date: 'Oct 12, 2024',
    readTime: '6 min read',
    category: 'Architecture',
  },
  {
    id: '2',
    title: 'Optimizing Rust for Production',
    excerpt: 'Practical tips for memory management and performance tuning in large-scale Rust applications.',
    date: 'Sep 28, 2024',
    readTime: '10 min read',
    category: 'Engineering',
  },
  {
    id: '3',
    title: 'Scaling Beyond 100M Users',
    excerpt: 'Lessons learned from building systems that handle massive concurrent traffic without breaking.',
    date: 'Aug 15, 2024',
    readTime: '8 min read',
    category: 'Scalability',
  },
];
