// lower _xx means darker for dark mode
// higher _xx means lighter for light mode

export const grayShadeL9xx = (themeName: string) => themeName === 'dark' ? 'text-gray-100' : 'text-gray-900';
export const grayShadeL8xx = (themeName: string) => themeName === 'dark' ? 'text-gray-200' : 'text-gray-800';
export const grayShadeL7xx = (themeName: string) => themeName === 'dark' ? 'text-gray-300' : 'text-gray-700';
export const grayShadeL6xx = (themeName: string) => themeName === 'dark' ? 'text-gray-400' : 'text-gray-600';
export const grayShadeL5xx = (themeName: string) => themeName === 'dark' ? 'text-gray-500' : 'text-gray-500';
export const grayShadeL4xx = (themeName: string) => themeName === 'dark' ? 'text-gray-600' : 'text-gray-400';
export const grayShadeL3xx = (themeName: string) => themeName === 'dark' ? 'text-gray-700' : 'text-gray-300';
export const grayShadeL2xx = (themeName: string) => themeName === 'dark' ? 'text-gray-800' : 'text-gray-200';
export const grayShadeL1xx = (themeName: string) => themeName === 'dark' ? 'text-gray-900' : 'text-gray-100';