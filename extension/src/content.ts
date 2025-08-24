// src/content.ts

chrome.runtime.onMessage.addListener((request, _sender, sendResponse) => {
  if (request.type === 'GET_JOB_DETAILS') {
    const jobTitle = document.querySelector('.jobs-unified-top-card__job-title')?.textContent?.trim() || '';
    const companyName = document.querySelector('.jobs-unified-top-card__company-name a')?.textContent?.trim() || '';
    const jobDescription = document.querySelector('#job-details')?.textContent?.trim() || '';

    sendResponse({
      title: jobTitle,
      company: companyName,
      description: jobDescription,
    });
  }
  return true; // Keeps the message channel open for an async response.
});