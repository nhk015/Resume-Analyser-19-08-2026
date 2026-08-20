# Product Discovery: AI Resume Analyzer & Job Recommendation System

**Document status:** Draft for product and engineering alignment  
**Date:** 19 August 2026  
**Product area:** Recruitment technology and career services

## 1. Executive Summary

The AI Resume Analyzer & Job Recommendation System helps students, fresh graduates, job seekers, career counselors, and placement officers turn a resume into clear, actionable career guidance. A user submits a resume, receives an analysis of its content and quality, sees extracted skills and experience insights, discovers relevant job opportunities, and receives targeted recommendations for improvement.

The MVP will focus on trustworthy resume parsing, explainable analysis, practical skill-gap identification, and job recommendations that are clearly connected to the user's profile. The product should support career decisions without presenting AI output as a guarantee of employment. It should provide a downloadable report that users and counselors can use in coaching, applications, and placement preparation.

## 2. Problem Statement

Many candidates do not know whether their resume communicates their experience effectively or which roles match their current capabilities. Existing resume tools often provide generic grammar feedback, while job boards return broad results that do not explain fit or identify the skills needed to qualify.

This creates several problems:

- Candidates submit resumes with unclear summaries, weak evidence of impact, inconsistent formatting, or missing role-specific keywords.
- Students and fresh graduates struggle to translate coursework, projects, internships, and extracurricular work into employable skills.
- Job seekers cannot easily understand why a role is recommended or what gaps prevent a stronger match.
- Career counselors and placement officers spend significant time manually reviewing resumes and creating individualized guidance.
- Users may receive opaque or overly confident AI feedback, which can mislead career decisions.

## 3. Business Objectives

### Primary objectives

1. Help users understand the strengths, weaknesses, and market relevance of their resumes.
2. Increase the quality and relevance of job applications through personalized recommendations.
3. Reduce the manual effort required for first-pass resume reviews by counselors and placement teams.
4. Convert resume analysis into specific, prioritized improvement actions.
5. Build user trust through transparent reasoning, confidence indicators, privacy controls, and human-review workflows.

### Success metrics for the MVP

- At least 90% of supported resumes produce a usable analysis without manual intervention.
- At least 85% of parsed resumes have correctly identified contact details, education, experience, and skills in evaluation samples.
- At least 70% of users rate recommendations as relevant or very relevant.
- At least 60% of users complete at least one recommended resume improvement action.
- Median time from upload to completed analysis is under 60 seconds for a standard resume.
- Counselors report a measurable reduction in time spent on initial resume screening.
- Fewer than 1% of generated reports expose data belonging to another user.

## 4. User Personas

### Persona 1: Student

- **Profile:** Undergraduate or postgraduate student with limited formal work experience.
- **Goals:** Understand suitable career paths, present projects and coursework effectively, and prepare for internships or campus placements.
- **Pain points:** Uncertainty about skills, lack of resume-writing experience, and difficulty interpreting job descriptions.
- **Needs:** Beginner-friendly explanations, project-to-skill mapping, entry-level recommendations, and a clear action plan.

### Persona 2: Job Seeker

- **Profile:** Fresh graduate or professional actively applying for jobs.
- **Goals:** Improve interview and application outcomes and target roles that match existing experience.
- **Pain points:** Generic feedback, repeated application rejection, and uncertainty about missing qualifications.
- **Needs:** Role-specific analysis, match explanations, missing-skill identification, and prioritized resume suggestions.

### Persona 3: Career Counselor

- **Profile:** Advisor supporting multiple students or candidates.
- **Goals:** Deliver consistent, evidence-based guidance efficiently and track client progress.
- **Pain points:** High review volume, repetitive resume feedback, and limited time for individualized coaching.
- **Needs:** Shareable reports, explainable findings, comparison over time, and an option to add human comments.

### Persona 4: Placement Officer

- **Profile:** University or training-organization staff member coordinating employer readiness and placement activity.
- **Goals:** Improve candidate readiness and align candidate pools with employer requirements.
- **Pain points:** Inconsistent resume quality, limited visibility into cohort skill gaps, and manual reporting.
- **Needs:** Candidate consent controls, aggregated insights, exportable reports, and role-readiness trends.

## 5. Product Scope

### MVP in scope

- Resume upload and text extraction for PDF and DOCX files.
- Resume parsing into structured sections.
- Resume quality and completeness analysis.
- Skills extraction and categorization.
- Experience evaluation, including projects and internships.
- AI-generated resume summary.
- Job recommendation based on resume, skills, experience, preferences, and location where available.
- Missing-skill identification for recommended roles.
- Prioritized resume improvement suggestions.
- Downloadable analysis report in PDF format.
- Basic user account, consent, data deletion, and report history.

### Explicitly out of scope for MVP

- Automatic job applications or submissions.
- Guaranteed job placement, hiring decisions, or candidate ranking for employers.
- Fully automated career counseling without the ability to review or question results.
- Video resume analysis and interview assessment.
- Background checks or verification of candidate claims.

## 6. Functional Requirements

### FR-1: Resume Submission

1. The system shall allow an authenticated user to upload a resume in supported PDF or DOCX format.
2. The system shall validate file type, file size, malware status, and readable text before analysis.
3. The system shall show upload, processing, success, and failure states.
4. The user shall be able to replace a resume and start a new analysis.
5. The system shall preserve the original file separately from extracted and generated content.
6. The system shall not begin analysis without the user's consent to process resume data.

### FR-2: Resume Analysis

1. The system shall identify standard sections including contact information, summary, education, experience, projects, skills, certifications, and awards where present.
2. The system shall evaluate completeness, clarity, consistency, relevance, and evidence of impact.
3. The system shall identify potential issues such as missing dates, unclear job titles, excessive length, weak action verbs, and unsupported claims.
4. Each major finding shall include an explanation and a confidence indicator where confidence is below the configured threshold.
5. The system shall distinguish detected facts from recommendations and shall not invent candidate experience.
6. The user shall be able to see the source resume text or section associated with a finding.

### FR-3: Skills Extraction

1. The system shall extract technical, domain, soft, language, and tool skills from the resume.
2. The system shall normalize equivalent terms, such as common abbreviations and spelling variants.
3. The system shall label skills by evidence source, such as work experience, project, education, or explicit skills section.
4. The user shall be able to correct, remove, or add skills before recommendations are generated.
5. The system shall show confidence or evidence for extracted skills and avoid treating a keyword alone as proof of proficiency.

### FR-4: Experience Evaluation

1. The system shall summarize total relevant experience when dates are available.
2. The system shall identify internships, projects, volunteer work, and employment separately where possible.
3. The system shall evaluate whether bullets describe actions, outcomes, scope, and measurable impact.
4. For students and fresh graduates, the system shall evaluate projects and coursework as potential experience evidence.
5. The system shall flag inconsistent or ambiguous dates without making unsupported assumptions.

### FR-5: Resume Summary Generation

1. The system shall generate a concise professional summary based only on information found in the resume and user-provided preferences.
2. The summary shall be editable before it is included in a report.
3. The system shall offer variants appropriate to the user's target role or career level.
4. The system shall identify generated text as AI-assisted content.
5. The system shall never add an unverified title, employer, certification, achievement, or years of experience.

### FR-6: Job Recommendation Engine

1. The system shall recommend relevant job roles using extracted skills, experience, education, seniority, location, work preference, and user-selected interests where available.
2. Each recommendation shall display a match score or fit band plus the factors that influenced it.
3. The system shall show matching qualifications, missing qualifications, and transferable skills separately.
4. The system shall support filtering by role, location, experience level, work arrangement, and date posted when job data supports those filters.
5. The system shall provide a reason when no strong recommendation is available.
6. Recommendations shall be refreshed when the user edits skills, experience, or target preferences.
7. Job data shall show its source and freshness date.

### FR-7: Missing Skill Identification

1. For each recommended role, the system shall identify high-value skills missing from or not evidenced in the resume.
2. The system shall prioritize gaps by relevance to the target role and likely impact on employability.
3. The system shall distinguish between missing evidence and genuinely missing skills.
4. The system shall provide a practical next step for each prioritized gap, such as a project, course, certification, or resume evidence prompt.
5. The system shall avoid presenting every job-description keyword as a mandatory gap.

### FR-8: Resume Improvement Suggestions

1. The system shall provide suggestions for content, structure, clarity, relevance, and formatting.
2. Suggestions shall be actionable and include before-and-after examples when the original content is suitable for comparison.
3. Suggestions shall be prioritized by expected impact and effort.
4. The user shall be able to dismiss, accept, or mark a suggestion as completed.
5. The system shall preserve user control over the final resume and shall not overwrite the source document automatically.

### FR-9: Downloadable Analysis Report

1. The user shall be able to generate and download a PDF report containing the analysis date, resume summary, score or quality indicators, extracted skills, experience findings, recommendations, skill gaps, and improvement plan.
2. The report shall clearly identify AI-generated content and analysis limitations.
3. A counselor or placement officer shall be able to share a report only with appropriate user consent.
4. Reports shall use an accessible layout and remain readable when printed.
5. The user shall be able to delete reports and associated resume data according to the retention policy.

### FR-10: Counselor and Placement Workflows

1. A user shall be able to share a time-limited report link or downloadable report with a counselor after giving consent.
2. Authorized counselors shall be able to add notes without changing the original AI analysis.
3. Placement officers shall be able to view only authorized candidate records.
4. Any future cohort-level reporting shall use aggregated or de-identified data unless explicit consent permits otherwise.
5. The system shall record access to shared reports for audit purposes.

## 7. Non Functional Requirements

### Performance and availability

- The upload response shall begin within 3 seconds under normal load.
- A standard resume analysis should complete within 60 seconds at the 95th percentile, excluding third-party outages.
- The service should target 99.5% monthly availability for the MVP.
- Long-running analysis shall be asynchronous and recoverable after transient failures.

### Security and privacy

- Data shall be encrypted in transit and at rest.
- Access shall use authenticated, authorized sessions with least-privilege permissions.
- Uploaded files shall be malware-scanned and stored with non-guessable identifiers.
- The product shall provide consent, retention, export, and deletion controls appropriate to the deployment jurisdiction.
- Personal data shall not be used to train models without explicit, separate consent.
- Logs shall avoid storing raw resume content unless required for an audited support workflow.

### Accuracy, fairness, and transparency

- The system shall measure parsing accuracy across file types, career levels, industries, and supported languages.
- Recommendations shall be explainable and must not use protected characteristics or obvious proxies for them.
- Users shall be able to report incorrect extraction, biased feedback, or unsuitable recommendations.
- The UI shall communicate that scores are guidance, not hiring predictions.
- Low-confidence results shall be surfaced for user review rather than stated as facts.

### Accessibility and usability

- The interface and downloadable report shall target WCAG 2.1 AA accessibility.
- The system shall support keyboard navigation, screen readers, clear focus states, sufficient contrast, and meaningful error messages.
- Findings shall use plain language and explain recruitment terminology.
- The core workflow shall work on current desktop and mobile browsers.

### Maintainability and observability

- Parsing, analysis, recommendation, and report-generation services shall be independently observable.
- The system shall log processing status, latency, failure category, and model version without exposing unnecessary personal data.
- AI prompts, models, taxonomies, and recommendation rules shall be versioned.
- The system shall support rollback of model or taxonomy changes.

## 8. User Stories

### Candidate stories

- As a student, I want to upload my resume so that I can understand how ready I am for internships and entry-level roles.
- As a job seeker, I want to see the skills extracted from my resume so that I can correct missing or inaccurate information.
- As a candidate, I want to know why a job was recommended so that I can decide whether it is worth applying for.
- As a candidate, I want to see missing skills for a target role so that I can create a focused development plan.
- As a candidate, I want concrete resume suggestions so that I can improve my applications without rewriting everything blindly.
- As a candidate, I want to edit generated content so that the final summary remains accurate and sounds like me.
- As a candidate, I want to download my report so that I can discuss it with a counselor or keep it for future applications.
- As a candidate, I want to delete my resume and reports so that I remain in control of my personal data.

### Counselor and placement stories

- As a counselor, I want to review a candidate's analysis with consent so that I can spend more time on high-value coaching.
- As a counselor, I want to add notes to a report so that human guidance is kept alongside AI findings.
- As a placement officer, I want to identify recurring skill gaps across an authorized cohort so that training can be planned effectively.
- As a placement officer, I want access controls and audit history so that candidate information is handled responsibly.

## 9. Acceptance Criteria

### Resume submission and processing

- Given a supported, readable PDF or DOCX file, when the user uploads it and consents, then the system creates an analysis job and shows its status.
- Given an unsupported, oversized, corrupted, or unsafe file, when the user uploads it, then the system rejects it with a clear corrective message and does not process it.
- Given a processing failure, when the system cannot complete analysis, then the user sees a recoverable error and can retry without duplicate reports.

### Analysis and skills

- Given a resume containing standard sections, when analysis completes, then the system displays detected sections and findings linked to relevant resume content.
- Given skills written with common abbreviations or variants, when extraction completes, then the system normalizes them while retaining the original wording as evidence.
- Given an uncertain extraction, when confidence is below the configured threshold, then the system marks it for user confirmation.

### Recommendations and gaps

- Given a completed analysis and target preferences, when recommendations are generated, then each result includes a fit explanation, source, freshness date, and matching or missing factors.
- Given a target role with a relevant skill gap, when the user opens the role details, then the system prioritizes the gap and provides at least one practical next step.
- Given edited skills or preferences, when the user requests refresh, then recommendations reflect the updated profile.

### Suggestions and reporting

- Given a weak or incomplete resume section, when suggestions are generated, then the system displays a prioritized, actionable recommendation without inventing facts.
- Given a completed report, when the user selects download, then a readable PDF is generated containing the latest approved analysis and clearly labeled AI-generated sections.
- Given a shared report, when an unauthorized user attempts access, then the system denies access and records the event.
- Given a deletion request, when the user confirms deletion, then the system removes the resume and associated reports within the documented retention period and confirms the result.

## 10. Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Incorrect parsing of layouts, tables, or scanned resumes | Misleading analysis | Support clear file limits, use OCR where appropriate, show evidence, and request confirmation for low-confidence fields. |
| Hallucinated summaries or suggestions | Candidate misrepresentation | Ground generation in extracted facts, validate output, label AI content, and keep all generated text editable. |
| Biased recommendations | Unfair career guidance | Exclude protected attributes, test across representative profiles, monitor outcomes, and provide a feedback and appeal path. |
| Stale or low-quality job data | Poor recommendations | Display source and freshness, validate feeds, remove expired listings, and provide a no-match explanation. |
| Privacy breach involving resumes | Serious user harm and regulatory exposure | Encrypt data, enforce access control, minimize logs, define retention, scan uploads, and audit sharing. |
| Overreliance on a score | Poor decisions or false confidence | Use fit bands with explanations, show limitations, and emphasize actions over a single score. |
| Third-party AI or job API outage | Workflow interruption | Use queues, retries, graceful degradation, health monitoring, and clear status messaging. |
| Low adoption by counselors or officers | Limited organizational value | Co-design workflows, provide shareable reports, measure time saved, and allow human notes. |
| Candidate claims are not verifiable | Employers may receive inaccurate information | State that the tool analyzes provided content only and does not verify credentials or experience. |

## 11. Future Enhancements

1. Resume tailoring against a selected job description with tracked keyword and evidence coverage.
2. Resume version management and comparison across applications.
3. Multilingual resume parsing and localized career guidance.
4. ATS compatibility simulation with transparent, non-guaranteed diagnostics.
5. Learning-path recommendations connected to trusted courses, projects, and certifications.
6. Interview preparation generated from the candidate's resume and target role.
7. Portfolio, GitHub, LinkedIn, and professional profile import with explicit consent.
8. Counselor dashboards with progress tracking, appointment context, and cohort-level skill trends.
9. Employer or institution integrations using privacy-preserving, role-based APIs.
10. Outcome measurement linking recommendations to applications, interviews, and user-reported outcomes.
11. Human-in-the-loop review for high-stakes institutional or employment workflows.
12. Personalization for career changes, return-to-work candidates, and non-traditional experience.

## 12. Open Product Decisions

- Which countries, job markets, languages, and privacy regulations are included in the first release?
- Which job data providers will be used, and what licensing and freshness guarantees do they provide?
- Will users receive a numeric score, a fit band, or both? How will the product prevent score misuse?
- What resume file size, page count, and scan-quality limits should be enforced?
- Which counselor and placement-officer roles, organizations, and consent workflows are required?
- What is the retention period for source resumes, extracted data, generated reports, and audit logs?
- Which model and taxonomy evaluation datasets will be approved before launch?

## 13. MVP Release Criteria

The MVP is ready for a controlled pilot when:

- Core upload, analysis, skills, recommendation, suggestion, and report workflows pass the acceptance criteria.
- Security, privacy, deletion, and role-access tests pass with no critical findings.
- Parsing and recommendation quality meet the agreed evaluation thresholds.
- Accessibility checks pass for the core workflow and report.
- A pilot group of candidates and counselors confirms that results are understandable, actionable, and appropriately qualified.
- Monitoring, incident handling, model versioning, and feedback collection are operational.
