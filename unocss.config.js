// unocss.config.js
import {
  defineConfig,
  presetUno,
  presetAttributify,
  presetIcons,
  presetTypography,
  presetWebFonts,
} from 'unocss'

export default defineConfig({
  presets: [
    presetUno(),
    presetAttributify(),
    presetIcons({
      scale: 1.2,
    }),
    presetTypography(),
    presetWebFonts({
      fonts: {
        sans: 'Inter:400,500,600,700',
        mono: 'Fira Code:400,700',
      },
    }),
  ],

  theme: {
    colors: {
      primary: '#2563eb',
      secondary: '#1e293b',
      accent: '#f59e0b',
      neutral: '#f3f4f6',
    },
  },

  shortcuts: {
    'btn-primary': 'bg-primary hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg shadow transition-all',
    'btn-secondary': 'bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium py-2 px-4 rounded-lg shadow-sm',
    'card': 'bg-white rounded-xl shadow-lg p-4 hover:shadow-xl transition-all',
    'input-base': 'border border-gray-300 rounded-lg px-3 py-2 focus:(border-primary ring-2 ring-blue-200) outline-none',
  },

  include: [
    './templates/**/*.html',
    './**/*.js',
    './**/*.py',
  ],
})
