// Утилиты для работы с темами

/**
 * Интерфейс для темы
 */
export interface Theme {
  name: string
  label: string
  description?: string
  colors: {
    primary: string
    secondary: string
    accent: string
    dark: string
    darkPage: string
    positive: string
    negative: string
    info: string
    warning: string
    background: string
    surface: string
    text: string
    textSecondary: string
    border: string
    shadow: string
    [key: string]: string
  }
  fonts: {
    family: string
    size: {
      xs: string
      sm: string
      md: string
      lg: string
      xl: string
      h1: string
      h2: string
      h3: string
      h4: string
      h5: string
      h6: string
    }
    weight: {
      light: number
      normal: number
      medium: number
      bold: number
    }
  }
  spacing: {
    xs: string
    sm: string
    md: string
    lg: string
    xl: string
    xxl: string
  }
  borderRadius: {
    sm: string
    md: string
    lg: string
    xl: string
  }
  shadows: {
    sm: string
    md: string
    lg: string
    xl: string
  }
  breakpoints: {
    xs: number
    sm: number
    md: number
    lg: number
    xl: number
  }
}

/**
 * Интерфейс для конфигурации темы
 */
export interface ThemeConfig {
  defaultTheme: string
  themes: Record<string, Theme>
  autoDetect: boolean
  storageKey: string
}

/**
 * Класс для управления темами
 */
export class ThemeManager {
  private config: ThemeConfig
  private currentTheme: string
  private themes: Record<string, Theme>
  private styleElement: HTMLStyleElement | null

  constructor(config?: Partial<ThemeConfig>) {
    this.config = {
      defaultTheme: 'light',
      themes: {},
      autoDetect: true,
      storageKey: 'vuege_theme',
      ...config
    }

    this.currentTheme = this.config.defaultTheme
    this.themes = { ...this.config.themes }
    this.styleElement = null

    this.init()
  }

  /**
   * Инициализирует менеджер тем
   */
  private init(): void {
    // Загружаем сохраненную тему
    const savedTheme = localStorage.getItem(this.config.storageKey)
    if (savedTheme && this.themes[savedTheme]) {
      this.currentTheme = savedTheme
    } else if (this.config.autoDetect) {
      // Автоопределение темы
      this.currentTheme = this.detectSystemTheme()
    }

    // Применяем тему
    this.applyTheme(this.currentTheme)
  }

  /**
   * Определяет системную тему
   */
  private detectSystemTheme(): string {
    if (typeof window !== 'undefined' && window.matchMedia) {
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
    }
    return 'light'
  }

  /**
   * Добавляет тему
   */
  addTheme(theme: Theme): void {
    this.themes[theme.name] = theme
  }

  /**
   * Удаляет тему
   */
  removeTheme(name: string): boolean {
    if (this.themes[name] && name !== this.config.defaultTheme) {
      delete this.themes[name]
      return true
    }
    return false
  }

  /**
   * Получает тему
   */
  getTheme(name?: string): Theme | null {
    const themeName = name || this.currentTheme
    return this.themes[themeName] || null
  }

  /**
   * Получает текущую тему
   */
  getCurrentTheme(): Theme | null {
    return this.getTheme(this.currentTheme)
  }

  /**
   * Устанавливает тему
   */
  setTheme(name: string): boolean {
    if (!this.themes[name]) {
      console.warn(`Theme "${name}" not found`)
      return false
    }

    this.currentTheme = name
    localStorage.setItem(this.config.storageKey, name)
    this.applyTheme(name)
    return true
  }

  /**
   * Переключает тему
   */
  toggleTheme(): string {
    const availableThemes = Object.keys(this.themes)
    
    if (availableThemes.length < 2) {
      return this.currentTheme
    }

    const currentIndex = availableThemes.indexOf(this.currentTheme)
    const nextIndex = (currentIndex + 1) % availableThemes.length
    const nextTheme = availableThemes[nextIndex]

    this.setTheme(nextTheme)
    return nextTheme
  }

  /**
   * Применяет тему
   */
  private applyTheme(name: string): void {
    const theme = this.themes[name]
    if (!theme) {
      return
    }

    // Создаем или обновляем элемент стилей
    if (!this.styleElement) {
      this.styleElement = document.createElement('style')
      this.styleElement.id = 'vuege-theme-styles'
      document.head.appendChild(this.styleElement)
    }

    // Генерируем CSS переменные
    const cssVariables = this.generateCSSVariables(theme)
    this.styleElement.textContent = `:root { ${cssVariables} }`

    // Обновляем атрибут data-theme
    document.documentElement.setAttribute('data-theme', name)

    // Эмитим событие изменения темы
    this.emitThemeChange(name, theme)
  }

  /**
   * Генерирует CSS переменные
   */
  private generateCSSVariables(theme: Theme): string {
    const variables: string[] = []

    // Цвета
    Object.entries(theme.colors).forEach(([key, value]) => {
      variables.push(`--color-${key}: ${value};`)
    })

    // Шрифты
    variables.push(`--font-family: ${theme.fonts.family};`)
    Object.entries(theme.fonts.size).forEach(([key, value]) => {
      variables.push(`--font-size-${key}: ${value};`)
    })
    Object.entries(theme.fonts.weight).forEach(([key, value]) => {
      variables.push(`--font-weight-${key}: ${value};`)
    })

    // Отступы
    Object.entries(theme.spacing).forEach(([key, value]) => {
      variables.push(`--spacing-${key}: ${value};`)
    })

    // Радиусы скругления
    Object.entries(theme.borderRadius).forEach(([key, value]) => {
      variables.push(`--border-radius-${key}: ${value};`)
    })

    // Тени
    Object.entries(theme.shadows).forEach(([key, value]) => {
      variables.push(`--shadow-${key}: ${value};`)
    })

    // Точки перелома
    Object.entries(theme.breakpoints).forEach(([key, value]) => {
      variables.push(`--breakpoint-${key}: ${value}px;`)
    })

    return variables.join('\n  ')
  }

  /**
   * Эмитит событие изменения темы
   */
  private emitThemeChange(name: string, theme: Theme): void {
    const event = new CustomEvent('themechange', {
      detail: { name, theme }
    })
    window.dispatchEvent(event)
  }

  /**
   * Получает доступные темы
   */
  getAvailableThemes(): string[] {
    return Object.keys(this.themes)
  }

  /**
   * Проверяет, поддерживается ли тема
   */
  isThemeSupported(name: string): boolean {
    return this.themes.hasOwnProperty(name)
  }

  /**
   * Получает цвет темы
   */
  getColor(colorName: string): string {
    const theme = this.getCurrentTheme()
    return theme?.colors[colorName] || ''
  }

  /**
   * Устанавливает цвет темы
   */
  setColor(colorName: string, value: string): void {
    const theme = this.getCurrentTheme()
    if (theme) {
      theme.colors[colorName] = value
      this.applyTheme(this.currentTheme)
    }
  }

  /**
   * Создает темную тему на основе светлой
   */
  createDarkTheme(baseTheme: Theme): Theme {
    const darkTheme: Theme = {
      ...baseTheme,
      name: `${baseTheme.name}-dark`,
      label: `${baseTheme.label} (Dark)`,
      colors: {
        ...baseTheme.colors,
        background: '#121212',
        surface: '#1e1e1e',
        text: '#ffffff',
        textSecondary: '#b0b0b0',
        border: '#333333',
        shadow: 'rgba(0, 0, 0, 0.3)'
      }
    }

    return darkTheme
  }

  /**
   * Создает светлую тему на основе темной
   */
  createLightTheme(baseTheme: Theme): Theme {
    const lightTheme: Theme = {
      ...baseTheme,
      name: `${baseTheme.name}-light`,
      label: `${baseTheme.label} (Light)`,
      colors: {
        ...baseTheme.colors,
        background: '#ffffff',
        surface: '#f5f5f5',
        text: '#000000',
        textSecondary: '#666666',
        border: '#e0e0e0',
        shadow: 'rgba(0, 0, 0, 0.1)'
      }
    }

    return lightTheme
  }

  /**
   * Экспортирует тему
   */
  exportTheme(name: string): Theme | null {
    return this.themes[name] || null
  }

  /**
   * Импортирует тему
   */
  importTheme(theme: Theme): void {
    this.addTheme(theme)
  }

  /**
   * Получает статистику тем
   */
  getStats(): Record<string, any> {
    const themes = Object.keys(this.themes)
    
    return {
      currentTheme: this.currentTheme,
      availableThemes: themes,
      totalThemes: themes.length,
      defaultTheme: this.config.defaultTheme,
      autoDetect: this.config.autoDetect
    }
  }
}

/**
 * Глобальный менеджер тем
 */
let globalThemeManager: ThemeManager | null = null

/**
 * Получает глобальный менеджер тем
 */
export function getGlobalThemeManager(): ThemeManager {
  if (!globalThemeManager) {
    globalThemeManager = new ThemeManager()
  }
  return globalThemeManager
}

/**
 * Устанавливает глобальный менеджер тем
 */
export function setGlobalThemeManager(manager: ThemeManager): void {
  globalThemeManager = manager
}

/**
 * Глобальные функции для быстрого доступа
 */
export const themeManager = {
  addTheme: (theme: Theme) => getGlobalThemeManager().addTheme(theme),
  removeTheme: (name: string) => getGlobalThemeManager().removeTheme(name),
  getTheme: (name?: string) => getGlobalThemeManager().getTheme(name),
  getCurrentTheme: () => getGlobalThemeManager().getCurrentTheme(),
  setTheme: (name: string) => getGlobalThemeManager().setTheme(name),
  toggleTheme: () => getGlobalThemeManager().toggleTheme(),
  getAvailableThemes: () => getGlobalThemeManager().getAvailableThemes(),
  isThemeSupported: (name: string) => getGlobalThemeManager().isThemeSupported(name),
  getColor: (colorName: string) => getGlobalThemeManager().getColor(colorName),
  setColor: (colorName: string, value: string) => getGlobalThemeManager().setColor(colorName, value),
  createDarkTheme: (baseTheme: Theme) => getGlobalThemeManager().createDarkTheme(baseTheme),
  createLightTheme: (baseTheme: Theme) => getGlobalThemeManager().createLightTheme(baseTheme),
  exportTheme: (name: string) => getGlobalThemeManager().exportTheme(name),
  importTheme: (theme: Theme) => getGlobalThemeManager().importTheme(theme),
  getStats: () => getGlobalThemeManager().getStats()
}

/**
 * Хук для использования менеджера тем в Vue компонентах
 */
export function useThemeManager() {
  const manager = getGlobalThemeManager()
  
  return {
    addTheme: manager.addTheme.bind(manager),
    removeTheme: manager.removeTheme.bind(manager),
    getTheme: manager.getTheme.bind(manager),
    getCurrentTheme: manager.getCurrentTheme.bind(manager),
    setTheme: manager.setTheme.bind(manager),
    toggleTheme: manager.toggleTheme.bind(manager),
    getAvailableThemes: manager.getAvailableThemes.bind(manager),
    isThemeSupported: manager.isThemeSupported.bind(manager),
    getColor: manager.getColor.bind(manager),
    setColor: manager.setColor.bind(manager),
    createDarkTheme: manager.createDarkTheme.bind(manager),
    createLightTheme: manager.createLightTheme.bind(manager),
    exportTheme: manager.exportTheme.bind(manager),
    importTheme: manager.importTheme.bind(manager),
    getStats: manager.getStats.bind(manager)
  }
}

