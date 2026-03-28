import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";
import { pluginFrames } from "@expressive-code/plugin-frames";

const pythonLearningTheme = {
  name: "python-learning",
  type: "dark",
  colors: {
    "editor.background": "#080b0f",
    "editor.foreground": "#e6edf3",
    "editor.lineHighlightBackground": "#161b22",
    "editorLineNumber.foreground": "#484f58",
    "editorLineNumber.activeForeground": "#E8922A",
    "editor.selectionBackground": "#2A555080",
    "editor.wordHighlightBackground": "#7A451030",
  },
  tokenColors: [
    // Keywords: class, def, return, import, from, if, for, while, with, as, raise
    {
      scope: [
        "keyword",
        "keyword.control",
        "keyword.operator.logical",
        "storage.type",
      ],
      settings: { foreground: "#E8922A", fontStyle: "bold" },
    },
    // Built-ins: print, len, range, isinstance, super
    {
      scope: ["support.function.builtin", "support.type.python"],
      settings: { foreground: "#5BA8A0" },
    },
    // Function and class definitions
    {
      scope: ["entity.name.function", "entity.name.class", "entity.name.type"],
      settings: { foreground: "#5BA8A0", fontStyle: "bold" },
    },
    // Decorators: @property, @classmethod, @staticmethod
    {
      scope: ["entity.name.function.decorator", "meta.decorator"],
      settings: { foreground: "#E8922A", fontStyle: "italic" },
    },
    // Strings
    {
      scope: ["string", "string.quoted", "string.template"],
      settings: { foreground: "#5AAF78" },
    },
    // f-string braces and interpolation
    {
      scope: [
        "meta.interpolation",
        "punctuation.definition.template-expression",
      ],
      settings: { foreground: "#E8922A" },
    },
    // Numbers
    {
      scope: ["constant.numeric"],
      settings: { foreground: "#C45C5C" },
    },
    // Constants: True, False, None
    {
      scope: ["constant.language", "constant.builtin"],
      settings: { foreground: "#C45C5C", fontStyle: "bold" },
    },
    // Comments
    {
      scope: ["comment", "comment.line", "comment.block"],
      settings: { foreground: "#848d97", fontStyle: "italic" },
    },
    // Self, cls
    {
      scope: [
        "variable.language.special.self",
        "variable.parameter.function.language.special",
      ],
      settings: { foreground: "#E8922A", fontStyle: "italic" },
    },
    // Parameters
    {
      scope: ["variable.parameter"],
      settings: { foreground: "#e6edf3" },
    },
    // Operators: =, +, -, *, /, %, ==, !=
    {
      scope: ["keyword.operator"],
      settings: { foreground: "#7A4510" },
    },
    // Punctuation: (), [], {}, :, ,
    {
      scope: ["punctuation", "meta.brace"],
      settings: { foreground: "#848d97" },
    },
    // Imports
    {
      scope: ["keyword.control.import", "keyword.control.from"],
      settings: { foreground: "#E8922A", fontStyle: "bold" },
    },
    // Exception types
    {
      scope: ["support.type.exception"],
      settings: { foreground: "#C45C5C" },
    },
    // Type hints
    {
      scope: ["meta.function.parameters.annotation", "support.type.typing"],
      settings: { foreground: "#5BA8A0", fontStyle: "italic" },
    },
  ],
};

export default defineConfig({
  base: process.env.NODE_ENV === "production" ? "/python-learning" : "/",
  devToolbar: { enabled: false },
  integrations: [
    starlight({
      title: "Python Learning",
      description: "A structured, test-driven approach to learning Python.",
      customCss: ["./src/styles/custom.css"],
      expressiveCode: {
        themes: [pythonLearningTheme],
        plugins: [pluginFrames()],
        styleOverrides: {
          codeBackground: "#080b0f",
          codePaddingBlock: "1rem",
          codePaddingInline: "1.2rem",
          borderRadius: "8px",
          borderColor: "transparent",
          boxShadow: "0 2px 12px rgba(0,0,0,0.5)",
          frames: {
            editorTabBarBackground: "#0f1117",
            editorTabBarBorderBottomColor: "#30363d",
            editorActiveTabBackground: "#080b0f",
            editorActiveTabBorderColor: "#E8922A",
            editorActiveTabForeground: "#E8922A",
          },
        },
      },
      social: [
        {
          icon: "github",
          label: "GitHub",
          href: "https://github.com/blackat/python-learning",
        },
      ],
      sidebar: [
        { label: "Home", link: "/" },
        {
          label: "Object Oriented Programming",
          items: [
            {
              label: "Foundation",
              items: [
                {
                  label: "Classes & Objects",
                  link: "/ch01_oop/01_foundation_classes/",
                },
                {
                  label: "Inheritance",
                  link: "/ch01_oop/02_foundation_inheritance/",
                },
                {
                  label: "Encapsulation",
                  link: "/ch01_oop/03_foundation_encapsulation/",
                },
              ],
            },
            { label: "Properties", link: "/ch01_oop/04_properties/" },
            { label: "Advanced", link: "/ch01_oop/05_advanced/" },
            { label: "Pythonic way", link: "/ch01_oop/06_pythonic/" },
          ],
        },
      ],
    }),
  ],
});
