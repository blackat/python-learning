import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";

const isProd = process.env.NODE_ENV === "production";

export default defineConfig({
  integrations: [
    starlight({
      title: "Python Learning",
      description: "A structured, test-driven approach to learning Python.",

      // Your brand colours
      customCss: ["./src/styles/custom.css"],

      // GitHub edit link
      editLink: {
        baseUrl:
          "https://github.com/blackat/python-learning/edit/main/docs-site/",
      },

      social: [
        {
          icon: "github",
          label: "GitHub",
          href: "https://github.com/blackat/python-learning",
        },
      ],

      sidebar: [
        {
          label: "Home",
          link: "/",
        },
        {
          label: "OOP",
          items: [
            {
              label: "Foundation",
              link: "/ch01_oop/foundation/",
            },
            {
              label: "Properties",
              link: "/ch01_oop/properties/",
            },
            {
              label: "Advanced",
              link: "/ch01_oop/advanced/",
            },
          ],
        },
      ],

      // Syntax highlighting via Shiki — much better than MkDocs
      expressiveCode: {
        themes: ["one-dark-pro"],
      },
    }),
  ],

  // GitHub Pages base path
  base: isProd ? "/python-learning" : "/",
  devToolbar: { enabled: false },
});
