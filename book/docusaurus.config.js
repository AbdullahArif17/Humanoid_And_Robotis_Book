// @ts-check
// `@type` JSDoc annotations allow IDEs and type checkers to understand your code
// and provide helpful autocompletion.

import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Humanoid & Robotics Book',
  tagline: 'A comprehensive guide to Physical AI and Humanoid Robotics',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://abdullaharif17.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub Pages: https://<USERNAME>.github.io/<REPO>/
  baseUrl: '/Humanoid_And_Robotis_Book/',

  // GitHub pages deployment config.
  organizationName: 'AbdullahArif17', // Usually your GitHub org/user name.
  projectName: 'Humanoid_And_Robotis_Book', // Usually your repo name.

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

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
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/AbdullahArif17/Humanoid_And_Robotis_Book/tree/main/',
        },
        blog: false, // Disable blog if not needed
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  // Custom fields that can be used throughout the site
  customFields: {
    backendUrl: process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000',
  },

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: 'Humanoid & Robotics Book',
        logo: {
          alt: 'Robotics Book Logo',
          src: 'img/logo.svg', // You can add a logo in static/img/
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Book',
          },
          {
            href: 'https://github.com/AbdullahArif17/Humanoid_And_Robotis_Book',
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
                label: 'Book Introduction',
                to: '/docs/intro',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'Stack Overflow',
                href: 'https://stackoverflow.com/questions/tagged/robotics',
              },
              {
                label: 'Discord',
                href: 'https://discordapp.com/invite/robotics',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/AbdullahArif17/Humanoid_And_Robotis_Book',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Humanoid & Robotics Book. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;


//  const config = {
//     // Change URL to your GitHub Pages URL
//     url: 'https://abdullaharif17.github.io',
//     baseUrl: '/Humanoid_And_Robotis_Book/',
//     trailingSlash: true,

//     // Update backend URL for GitHub Pages
//     customFields: {
//       backendUrl: process.env.REACT_APP_BACKEND_URL || 'https://your-backend-domain.com',
//     },

//     // Enable trailing slashes for GitHub Pages
//     trailingSlash: true,

//     // Add sitemap for SEO
//     sitemap: {
//       changefreq: 'weekly',
//       priority: 0.5,
//       ignorePatterns: ['/tags/**'],
//       filename: 'sitemap.xml',
//     },
//   };

//   module.exports = config;