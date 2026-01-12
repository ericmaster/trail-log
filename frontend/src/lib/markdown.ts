import { marked } from 'marked';
import { locale } from 'svelte-i18n';
import { get } from 'svelte/store';

/**
 * Fetches and parses markdown content based on the current locale
 * @param contentName - Name of the markdown file (without extension)
 * @returns Parsed HTML content
 */
export interface MarkdownContent {
    title: string;
    html: string;
}

/**
 * Fetches and parses markdown content based on the current locale
 * @param contentName - Name of the markdown file (without extension)
 * @returns Object containing title and parsed HTML content
 */
export async function loadMarkdownContent(contentName: string): Promise<MarkdownContent> {
    const currentLocale = get(locale) || 'en';
    const localePrefix = currentLocale.startsWith('es') ? 'es' : 'en';

    try {
        const response = await fetch(`/content/${localePrefix}/${contentName}.md`);
        if (!response.ok) {
            throw new Error(`Failed to load ${contentName}.md`);
        }
        const text = await response.text();

        // Simple frontmatter parser
        const match = text.match(/^---\n([\s\S]+?)\n---\n([\s\S]*)$/);
        let title = '';
        let markdownBody = text;

        if (match) {
            const frontmatter = match[1];
            markdownBody = match[2];

            // Extract title
            const titleMatch = frontmatter.match(/title:\s*(.+)/);
            if (titleMatch) {
                title = titleMatch[1].trim();
            }
        }

        // Return title and parsed HTML
        return {
            title,
            html: await marked(markdownBody)
        };
    } catch (error) {
        console.error(`Error loading markdown content for ${contentName}:`, error);
        return {
            title: 'Error',
            html: `<p>Error loading content. Please try again later.</p>`
        };
    }
}
