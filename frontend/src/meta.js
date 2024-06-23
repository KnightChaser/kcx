// frontend/meta.js

// This file is used to add meta tags to the document head based on the environment variables.
// Depending on the environment variable values, the meta tags are added to the document head.
// (Allowing the browser to load the resources over HTTPS, if the backend API URL is HTTPS.)

const backendApiUrl = import.meta.env.VITE_BACKEND_API_URL;

if (backendApiUrl && backendApiUrl.startsWith('https')) {
    const metaTag = document.createElement('meta');
    metaTag.setAttribute('charset', 'UTF-8');
    metaTag.setAttribute('http-equiv', 'Content-Security-Policy');
    metaTag.setAttribute('content', 'upgrade-insecure-requests');
    document.head.appendChild(metaTag);

    console.log(`Since the backend API URL is ${backendApiUrl}, the Content-Security-Policy meta tag has been added to the document head.`);
}