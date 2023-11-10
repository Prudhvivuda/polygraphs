import { defineConfig } from "vitepress";

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "PolyGraphs",
  description: "Combatting Networks of Ignorance in the Misinformation Age",

  base: '/polygraphs/',
  cleanUrls: true,

  markdown: {
    math: true,
  },

  themeConfig: {
    // logo: { src: "/vitepress-logo-mini.svg", width: 24, height: 24 },

    nav: [
      {
        text: "Guide",
        link: "/guide/introduction/what-is-polygraphs",
        activeMatch: "/guide/",
      },
      {
        text: "Reference",
        link: "/reference/simulation-config",
        activeMatch: "/reference/",
      },
    ],

    sidebar: {
      "/guide/": { items: sidebarGuide() },
      "/reference/": { items: sidebarReference() },
    },

    socialLinks: [
      {
        icon: "github",
        link: "https://github.com/alexandroskoliousis/polygraphs",
      },
    ],
  },
});

function sidebarGuide() {
  return [
    {
      text: "Introduction",
      collapsed: false,
      items: [
        {
          text: "What is PolyGraphs?",
          link: "/guide/introduction/what-is-polygraphs",
        },
        {
          text: "Getting Started",
          link: "/guide/introduction/getting-started",
        },
      ],
    },
    {
      text: "Simulations",
      collapsed: false,
      items: [
        {
          text: "Running Simulations",
          link: "/guide/simulations/running-simulations",
        },
        {
          text: "Gathering Results",
          link: "/guide/simulations/gathering-results",
        },
        {
          text: "Batch Jobs",
          link: "/guide/simulations/batch-jobs",
        },
      ],
    },
    {
      text: "Analysis",
      collapsed: false,
      items: [
        { text: "Proportions", link: "/guide/analysis/proportions" },
        { text: "Steps", link: "/guide/analysis/steps" },
        { text: "Individual Nodes", link: "/guide/analysis/individual-nodes" },
        { text: "Network Analysis", link: "/guide/analysis/network" },
      ],
    },
    {
      text: "OPs",
      collapsed: false,
      items: [
        { text: "PolyGraph OPs", link: "/guide/ops/polygraph-ops" },
        { text: "Complex OPs", link: "/guide/ops/complex" },
        { text: "Creating a Custom OP", link: "/guide/ops/custom" },
      ],
    },
    {
      text: "Graphs",
      collapsed: false,
      items: [
        { text: "SNAP Networks", link: "/guide/graphs/snap-networks" },
        {
          text: "Custom Graphs",
          link: "/guide/graphs/custom-networks",
        },
      ],
    },
    {
      text: "Reference",
      base: "/reference/",
      link: "simulation-config",
    },
  ];
}

function sidebarReference() {
  return [
    {
      text: "Reference",
      items: [
        { text: "Simulation Config", link: "/reference/simulation-config" },
        { text: "Network Config", link: "/reference/network-config" },
        { text: "Explorables", link: "/reference/explorables" },
      ],
    },
    {
      text: "Guide",
      base: "/guide/",
      link: "/introduction/what-is-polygraphs",
    },
  ];
}
