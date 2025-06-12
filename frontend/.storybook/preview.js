import { themes } from '@storybook/theming';
import { withThemeProvider } from 'storybook-addon-theme-provider';
import { withRtl } from 'storybook-addon-rtl';
import { withA11y } from '@storybook/addon-a11y';
import { withViewport } from '@storybook/addon-viewport';
import { withNextRouter } from 'storybook-addon-next-router';
import { withI18n } from 'storybook-addon-i18n';
import { withKnobs } from '@storybook/addon-knobs';
import { withConsole } from '@storybook/addon-console';
import { withBackgrounds } from '@storybook/addon-backgrounds';
import { withInfo } from '@storybook/addon-info';
import { withTests } from '@storybook/addon-jest';
import { withActions } from '@storybook/addon-actions';
import { withLinks } from '@storybook/addon-links';
import { withNotes } from '@storybook/addon-notes';
import { withOptions } from '@storybook/addon-options';
import { withCssResources } from '@storybook/addon-cssresources';
import { withDesign } from 'storybook-addon-designs';
import { withContexts } from '@storybook/addon-contexts';
import { withPerformance } from 'storybook-addon-performance';
import { withResponsive } from 'storybook-addon-responsive';
import { withScreenshot } from 'storybook-addon-screenshot';
import { withSource } from '@storybook/addon-storysource';
import { withStorybookStyles } from 'storybook-addon-styles';
import { withThemes } from 'storybook-addon-themes';
import { withViewport as withViewportAddon } from '@storybook/addon-viewport';
import { withKnobs as withKnobsAddon } from '@storybook/addon-knobs';
import { withA11y as withA11yAddon } from '@storybook/addon-a11y';
import { withConsole as withConsoleAddon } from '@storybook/addon-console';
import { withBackgrounds as withBackgroundsAddon } from '@storybook/addon-backgrounds';
import { withInfo as withInfoAddon } from '@storybook/addon-info';
import { withTests as withTestsAddon } from '@storybook/addon-jest';
import { withActions as withActionsAddon } from '@storybook/addon-actions';
import { withLinks as withLinksAddon } from '@storybook/addon-links';
import { withNotes as withNotesAddon } from '@storybook/addon-notes';
import { withOptions as withOptionsAddon } from '@storybook/addon-options';
import { withCssResources as withCssResourcesAddon } from '@storybook/addon-cssresources';
import { withDesign as withDesignAddon } from 'storybook-addon-designs';
import { withContexts as withContextsAddon } from '@storybook/addon-contexts';
import { withPerformance as withPerformanceAddon } from 'storybook-addon-performance';
import { withResponsive as withResponsiveAddon } from 'storybook-addon-responsive';
import { withScreenshot as withScreenshotAddon } from 'storybook-addon-screenshot';
import { withSource as withSourceAddon } from '@storybook/addon-storysource';
import { withStorybookStyles as withStorybookStylesAddon } from 'storybook-addon-styles';
import { withThemes as withThemesAddon } from 'storybook-addon-themes';
import { withViewport as withViewportAddon2 } from '@storybook/addon-viewport';
import { withKnobs as withKnobsAddon2 } from '@storybook/addon-knobs';
import { withA11y as withA11yAddon2 } from '@storybook/addon-a11y';
import { withConsole as withConsoleAddon2 } from '@storybook/addon-console';
import { withBackgrounds as withBackgroundsAddon2 } from '@storybook/addon-backgrounds';
import { withInfo as withInfoAddon2 } from '@storybook/addon-info';
import { withTests as withTestsAddon2 } from '@storybook/addon-jest';
import { withActions as withActionsAddon2 } from '@storybook/addon-actions';
import { withLinks as withLinksAddon2 } from '@storybook/addon-links';
import { withNotes as withNotesAddon2 } from '@storybook/addon-notes';
import { withOptions as withOptionsAddon2 } from '@storybook/addon-options';
import { withCssResources as withCssResourcesAddon2 } from '@storybook/addon-cssresources';
import { withDesign as withDesignAddon2 } from 'storybook-addon-designs';
import { withContexts as withContextsAddon2 } from '@storybook/addon-contexts';
import { withPerformance as withPerformanceAddon2 } from 'storybook-addon-performance';
import { withResponsive as withResponsiveAddon2 } from 'storybook-addon-responsive';
import { withScreenshot as withScreenshotAddon2 } from 'storybook-addon-screenshot';
import { withSource as withSourceAddon2 } from '@storybook/addon-storysource';
import { withStorybookStyles as withStorybookStylesAddon2 } from 'storybook-addon-styles';
import { withThemes as withThemesAddon2 } from 'storybook-addon-themes';

export const decorators = [
  withThemeProvider,
  withRtl,
  withA11y,
  withViewport,
  withNextRouter,
  withI18n,
  withKnobs,
  withConsole,
  withBackgrounds,
  withInfo,
  withTests,
  withActions,
  withLinks,
  withNotes,
  withOptions,
  withCssResources,
  withDesign,
  withContexts,
  withPerformance,
  withResponsive,
  withScreenshot,
  withSource,
  withStorybookStyles,
  withThemes,
];

export const parameters = {
  actions: { argTypesRegex: '^on[A-Z].*' },
  controls: {
    matchers: {
      color: /(background|color)$/i,
      date: /Date$/,
    },
  },
  darkMode: {
    dark: { ...themes.dark },
    light: { ...themes.normal },
  },
  backgrounds: {
    default: 'light',
    values: [
      {
        name: 'light',
        value: '#ffffff',
      },
      {
        name: 'dark',
        value: '#1a1a1a',
      },
    ],
  },
  viewport: {
    viewports: {
      mobile: {
        name: 'Mobile',
        styles: {
          width: '360px',
          height: '640px',
        },
      },
      tablet: {
        name: 'Tablet',
        styles: {
          width: '768px',
          height: '1024px',
        },
      },
      desktop: {
        name: 'Desktop',
        styles: {
          width: '1366px',
          height: '768px',
        },
      },
    },
  },
  i18n: {
    locales: ['ar', 'en'],
    defaultLocale: 'ar',
  },
  rtl: {
    defaultDirection: 'rtl',
  },
  a11y: {
    config: {
      rules: [
        {
          id: 'color-contrast',
          enabled: true,
        },
      ],
    },
  },
  docs: {
    theme: themes.dark,
  },
}; 