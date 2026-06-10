export function stripPunctuation(text: string): string {
	const punctuationRegex = /[!"#$%&'«»()*+,\-./:;<=>?@[\\\]^_`{|}~]/g;
	return text.replace(punctuationRegex, '');
}
