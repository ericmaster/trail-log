import { register, init, getLocaleFromNavigator } from 'svelte-i18n';

register('en', () => import('./en.json'));
register('es', () => import('./es.json'));

const getInitialLocale = () => {
    const locale = getLocaleFromNavigator();
    if (locale) {
        const baseLocale = locale.split('-')[0].toLowerCase();
        if (baseLocale === 'es') return 'es';
    }
    return 'en';
};

init({
    fallbackLocale: 'en',
    initialLocale: getInitialLocale(),
});

