import { BlogPost } from './types';

export const BLOG_POSTS: BlogPost[] = [
  {
    title: 'The Future of Distributed Systems',
    excerpt: 'Exploring the transition from centralized clouds to decentralized edge computing networks.',
    date: 'Oct 12, 2024',
    readTime: '6 min read',
    category: 'Architecture',
  },
  {
    title: 'Optimizing Rust for Production',
    excerpt: 'Practical tips for memory management and performance tuning in large-scale Rust applications.',
    date: 'Sep 28, 2024',
    readTime: '10 min read',
    category: 'Engineering',
  },
  {
    title: 'Scaling Beyond 100M Users',
    excerpt: 'Lessons learned from building systems that handle massive concurrent traffic without breaking.',
    date: 'Aug 15, 2024',
    readTime: '8 min read',
    category: 'Scalability',
  },
];
