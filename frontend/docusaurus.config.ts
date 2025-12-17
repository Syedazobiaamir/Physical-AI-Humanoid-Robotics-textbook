import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';
import * as dotenv from 'dotenv';

// Load environment variables from .env file
dotenv.config();

const config: Config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'An AI-Native Textbook for Physical AI and Humanoid Robotics',
  favicon: 'img/favicon.svg',

  url: 'https://your-username.github.io',
  baseUrl: '/',

  organizationName: 'your-username',
  projectName: 'physical-ai-textbook',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Custom fields for runtime configuration
  customFields: {
    // Backend API URL - Set via environment variable or update directly
    // For Vercel deployment: Set DOCUSAURUS_API_BASE_URL in Vercel dashboard
    apiBaseUrl: process.env.DOCUSAURUS_API_BASE_URL || '',
    // Clerk Publishable Key - Set via environment variable
    // Get from https://dashboard.clerk.com
    clerkPublishableKey: process.env.CLERK_PUBLISHABLE_KEY || '',
  },

  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ur'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/your-username/physical-ai-textbook/tree/main/',
          remarkPlugins: [],
          rehypePlugins: [],
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',
    navbar: {
      title: 'Physical AI & Humanoid Robotics',
      logo: {
        alt: 'Physical AI Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Book Chapters',
        },
        
      ],
    },
    footer: {
      style: 'light',
      links: [
        {
          title: 'About Book',
          items: [
            {
              label: 'Book Chapters',
              to: '/docs/intro',
            },
          ],
        },
        {
          title: 'Resources',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/your-username/physical-ai-textbook',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics Textbook.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['python', 'bash', 'cpp', 'cmake', 'yaml'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
