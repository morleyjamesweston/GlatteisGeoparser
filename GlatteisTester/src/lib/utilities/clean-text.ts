// removes all content inside < > < /> tags
export function removeHtmlContent(text: string) {
	return text.replace(/<[^>]*>/g, ' ');
}
