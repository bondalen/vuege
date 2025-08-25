// Утилиты для работы с цветами

/**
 * Преобразует HEX цвет в RGB
 */
export function hexToRgb(hex: string): { r: number; g: number; b: number } | null {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex)
  if (!result) return null
  
  return {
    r: parseInt(result[1], 16),
    g: parseInt(result[2], 16),
    b: parseInt(result[3], 16)
  }
}

/**
 * Преобразует RGB в HEX
 */
export function rgbToHex(r: number, g: number, b: number): string {
  const toHex = (n: number) => {
    const hex = n.toString(16)
    return hex.length === 1 ? '0' + hex : hex
  }
  
  return `#${toHex(r)}${toHex(g)}${toHex(b)}`
}

/**
 * Преобразует HEX цвет в HSL
 */
export function hexToHsl(hex: string): { h: number; s: number; l: number } | null {
  const rgb = hexToRgb(hex)
  if (!rgb) return null
  
  return rgbToHsl(rgb.r, rgb.g, rgb.b)
}

/**
 * Преобразует RGB в HSL
 */
export function rgbToHsl(r: number, g: number, b: number): { h: number; s: number; l: number } {
  r /= 255
  g /= 255
  b /= 255
  
  const max = Math.max(r, g, b)
  const min = Math.min(r, g, b)
  let h = 0
  let s = 0
  const l = (max + min) / 2
  
  if (max !== min) {
    const d = max - min
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min)
    
    switch (max) {
      case r:
        h = (g - b) / d + (g < b ? 6 : 0)
        break
      case g:
        h = (b - r) / d + 2
        break
      case b:
        h = (r - g) / d + 4
        break
    }
    
    h /= 6
  }
  
  return {
    h: Math.round(h * 360),
    s: Math.round(s * 100),
    l: Math.round(l * 100)
  }
}

/**
 * Преобразует HSL в RGB
 */
export function hslToRgb(h: number, s: number, l: number): { r: number; g: number; b: number } {
  h /= 360
  s /= 100
  l /= 100
  
  const hue2rgb = (p: number, q: number, t: number) => {
    if (t < 0) t += 1
    if (t > 1) t -= 1
    if (t < 1/6) return p + (q - p) * 6 * t
    if (t < 1/2) return q
    if (t < 2/3) return p + (q - p) * (2/3 - t) * 6
    return p
  }
  
  let r, g, b
  
  if (s === 0) {
    r = g = b = l
  } else {
    const q = l < 0.5 ? l * (1 + s) : l + s - l * s
    const p = 2 * l - q
    
    r = hue2rgb(p, q, h + 1/3)
    g = hue2rgb(p, q, h)
    b = hue2rgb(p, q, h - 1/3)
  }
  
  return {
    r: Math.round(r * 255),
    g: Math.round(g * 255),
    b: Math.round(b * 255)
  }
}

/**
 * Преобразует HSL в HEX
 */
export function hslToHex(h: number, s: number, l: number): string {
  const rgb = hslToRgb(h, s, l)
  return rgbToHex(rgb.r, rgb.g, rgb.b)
}

/**
 * Осветляет цвет на указанный процент
 */
export function lighten(hex: string, percent: number): string {
  const hsl = hexToHsl(hex)
  if (!hsl) return hex
  
  hsl.l = Math.min(100, hsl.l + percent)
  return hslToHex(hsl.h, hsl.s, hsl.l)
}

/**
 * Затемняет цвет на указанный процент
 */
export function darken(hex: string, percent: number): string {
  const hsl = hexToHsl(hex)
  if (!hsl) return hex
  
  hsl.l = Math.max(0, hsl.l - percent)
  return hslToHex(hsl.h, hsl.s, hsl.l)
}

/**
 * Изменяет насыщенность цвета
 */
export function saturate(hex: string, percent: number): string {
  const hsl = hexToHsl(hex)
  if (!hsl) return hex
  
  hsl.s = Math.max(0, Math.min(100, hsl.s + percent))
  return hslToHex(hsl.h, hsl.s, hsl.l)
}

/**
 * Уменьшает насыщенность цвета
 */
export function desaturate(hex: string, percent: number): string {
  return saturate(hex, -percent)
}

/**
 * Создает монохромную версию цвета
 */
export function grayscale(hex: string): string {
  return desaturate(hex, 100)
}

/**
 * Инвертирует цвет
 */
export function invert(hex: string): string {
  const rgb = hexToRgb(hex)
  if (!rgb) return hex
  
  return rgbToHex(255 - rgb.r, 255 - rgb.g, 255 - rgb.b)
}

/**
 * Смешивает два цвета
 */
export function mix(color1: string, color2: string, weight: number = 0.5): string {
  const rgb1 = hexToRgb(color1)
  const rgb2 = hexToRgb(color2)
  
  if (!rgb1 || !rgb2) return color1
  
  const r = Math.round(rgb1.r * weight + rgb2.r * (1 - weight))
  const g = Math.round(rgb1.g * weight + rgb2.g * (1 - weight))
  const b = Math.round(rgb1.b * weight + rgb2.b * (1 - weight))
  
  return rgbToHex(r, g, b)
}

/**
 * Проверяет, является ли цвет светлым
 */
export function isLight(hex: string): boolean {
  const hsl = hexToHsl(hex)
  if (!hsl) return false
  
  return hsl.l > 50
}

/**
 * Проверяет, является ли цвет темным
 */
export function isDark(hex: string): boolean {
  return !isLight(hex)
}

/**
 * Получает контрастный цвет (черный или белый)
 */
export function getContrastColor(hex: string): string {
  return isLight(hex) ? '#000000' : '#ffffff'
}

/**
 * Вычисляет контраст между двумя цветами
 */
export function getContrastRatio(color1: string, color2: string): number {
  const rgb1 = hexToRgb(color1)
  const rgb2 = hexToRgb(color2)
  
  if (!rgb1 || !rgb2) return 1
  
  const luminance1 = getLuminance(rgb1.r, rgb1.g, rgb1.b)
  const luminance2 = getLuminance(rgb2.r, rgb2.g, rgb2.b)
  
  const lighter = Math.max(luminance1, luminance2)
  const darker = Math.min(luminance1, luminance2)
  
  return (lighter + 0.05) / (darker + 0.05)
}

/**
 * Вычисляет яркость цвета
 */
export function getLuminance(r: number, g: number, b: number): number {
  const [rs, gs, bs] = [r, g, b].map(c => {
    c = c / 255
    return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4)
  })
  
  return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs
}

/**
 * Генерирует случайный цвет
 */
export function generateRandomColor(): string {
  const hue = Math.floor(Math.random() * 360)
  const saturation = 50 + Math.floor(Math.random() * 30)
  const lightness = 40 + Math.floor(Math.random() * 20)
  
  return hslToHex(hue, saturation, lightness)
}

/**
 * Генерирует палитру цветов
 */
export function generateColorPalette(baseColor: string, count: number = 5): string[] {
  const hsl = hexToHsl(baseColor)
  if (!hsl) return Array(count).fill(baseColor)
  
  const palette: string[] = []
  const step = 360 / count
  
  for (let i = 0; i < count; i++) {
    const hue = (hsl.h + i * step) % 360
    palette.push(hslToHex(hue, hsl.s, hsl.l))
  }
  
  return palette
}

/**
 * Преобразует цвет в RGBA
 */
export function hexToRgba(hex: string, alpha: number = 1): string {
  const rgb = hexToRgb(hex)
  if (!rgb) return hex
  
  return `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, ${alpha})`
}

/**
 * Проверяет, является ли строка валидным HEX цветом
 */
export function isValidHexColor(hex: string): boolean {
  return /^#?([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/.test(hex)
}

/**
 * Нормализует HEX цвет (добавляет # если отсутствует)
 */
export function normalizeHexColor(hex: string): string {
  if (hex.startsWith('#')) {
    return hex
  }
  return `#${hex}`
}