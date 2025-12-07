import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

// Determine if we're in production (GitHub Pages) or local development
const isProduction = process.env.NODE_ENV === 'production';

// GitHub Pages configuration
const githubOrgName = 'AbdullahArif17'; // Set directly for local development
const githubProjectName = 'Humanoid_And_Robotis_Book'; // Set directly for local development
const githubRepoUrl = process.env.GITHUB_REPO_URL || `https://github.com/${githubOrgName}/${githubProjectName}`;
const githubPagesUrl = process.env.GITHUB_PAGES_URL || `https://${githubOrgName.toLowerCase()}.github.io`;
const projectBaseUrl = process.env.PROJECT_BASE_URL || `/${githubProjectName}/`;

const config: Config = {
  title: 'Humanoid & Robotics Book',
  tagline: 'Physical AI & Humanoid Robotics: From Theory to Autonomous Action',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: isProduction ? githubPagesUrl : 'http://localhost:3000',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: isProduction ? projectBaseUrl : '/',

  // GitHub pages deployment config.
  organizationName: githubOrgName,
  projectName: githubProjectName,

  onBrokenLinks: 'throw',
  
  markdown: {
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
  },

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          // Remove this to remove the "edit this page" links.
          editUrl: `${githubRepoUrl}/tree/main/book/`,
        },
        blog: { 
          showReadingTime: true,
          editUrl: `${githubRepoUrl}/tree/main/book/`,
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Humanoid & Robotics Book',
      logo: {
        alt: 'Humanoid & Robotics Book Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Book Modules',
        },
        {to: '/blog', label: 'Blog', position: 'left'},
        {to: '/chatbot-page', label: 'Chatbot', position: 'left'}, // Added Chatbot link
        {
          href: githubRepoUrl,
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Introduction',
              to: '/docs/intro',
            },
            {
              label: 'Chatbot',
              to: '/chatbot-page',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'GitHub Discussions',
              href: `${githubRepoUrl}/discussions`,
            },
            {
              label: 'Issues',
              href: `${githubRepoUrl}/issues`,
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'Blog',
              to: '/blog',
            },
            {
              label: 'GitHub',
              href: githubRepoUrl,
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Humanoid & Robotics Book. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['python', 'bash', 'json', 'yaml'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;