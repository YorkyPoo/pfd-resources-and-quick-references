// Pre-Cache Service Worker for Poquoson Fire & Rescue Protocols
// Generated: 20260910-041124
// Caches ALL protocols on first visit for full offline access

const CACHE_NAME = "pfd-protocols-v20260910-041124";

const PRECACHE_URLS = [
    "/pfd-resources-and-quick-references/404.html",
    "/pfd-resources-and-quick-references/index.html",
    "/pfd-resources-and-quick-references/medications.html",
    "/pfd-resources-and-quick-references/pediatric-dosing/calculator.html",
    "/pfd-resources-and-quick-references/pediatric-dosing/dosing-tables.html",
    "/pfd-resources-and-quick-references/pediatric-dosing/index.html",
    "/pfd-resources-and-quick-references/personnel-policies/other/personnel-policy-manual.html",
    "/pfd-resources-and-quick-references/pharmacology/Adenosine.html",
    "/pfd-resources-and-quick-references/pharmacology/Albuterol.html",
    "/pfd-resources-and-quick-references/pharmacology/Amiodarone.html",
    "/pfd-resources-and-quick-references/pharmacology/Aspirin.html",
    "/pfd-resources-and-quick-references/pharmacology/Atropine Sulfate.html",
    "/pfd-resources-and-quick-references/pharmacology/Calcium Chloride.html",
    "/pfd-resources-and-quick-references/pharmacology/Dextrose.html",
    "/pfd-resources-and-quick-references/pharmacology/Diphenhydramine.html",
    "/pfd-resources-and-quick-references/pharmacology/Epinephrine.html",
    "/pfd-resources-and-quick-references/pharmacology/Etomidate.html",
    "/pfd-resources-and-quick-references/pharmacology/Fentanyl.html",
    "/pfd-resources-and-quick-references/pharmacology/Furosemide.html",
    "/pfd-resources-and-quick-references/pharmacology/Glucagon.html",
    "/pfd-resources-and-quick-references/pharmacology/Haloperidol.html",
    "/pfd-resources-and-quick-references/pharmacology/Hydroxocobalamin.html",
    "/pfd-resources-and-quick-references/pharmacology/Ipratropium Bromide.html",
    "/pfd-resources-and-quick-references/pharmacology/Ketamine.html",
    "/pfd-resources-and-quick-references/pharmacology/Ketorolac.html",
    "/pfd-resources-and-quick-references/pharmacology/Lidocaine.html",
    "/pfd-resources-and-quick-references/pharmacology/Magnesium Sulfate.html",
    "/pfd-resources-and-quick-references/pharmacology/Methylprednisolone.html",
    "/pfd-resources-and-quick-references/pharmacology/Midazolam.html",
    "/pfd-resources-and-quick-references/pharmacology/Morphine Sulfate.html",
    "/pfd-resources-and-quick-references/pharmacology/Naloxone.html",
    "/pfd-resources-and-quick-references/pharmacology/Nitroglycerin.html",
    "/pfd-resources-and-quick-references/pharmacology/Nitroglycerine.html",
    "/pfd-resources-and-quick-references/pharmacology/Norepinephrine.html",
    "/pfd-resources-and-quick-references/pharmacology/Ondansetron.html",
    "/pfd-resources-and-quick-references/pharmacology/Rocuronium.html",
    "/pfd-resources-and-quick-references/pharmacology/Sodium Bicarbonate.html",
    "/pfd-resources-and-quick-references/pharmacology/Succinylcholine.html",
    "/pfd-resources-and-quick-references/pharmacology/Vecuronium.html",
    "/pfd-resources-and-quick-references/pharmacology/Ziprasidone.html",
    "/pfd-resources-and-quick-references/procedures/CPAP.html",
    "/pfd-resources-and-quick-references/procedures/Capnography.html",
    "/pfd-resources-and-quick-references/procedures/Chest_Decompression.html",
    "/pfd-resources-and-quick-references/procedures/Endotracheal_Intubation.html",
    "/pfd-resources-and-quick-references/procedures/Intraosseous_Access.html",
    "/pfd-resources-and-quick-references/procedures/Medical_Devices_Pumps.html",
    "/pfd-resources-and-quick-references/procedures/Medication_Administration.html",
    "/pfd-resources-and-quick-references/procedures/Nasogastric_Tube.html",
    "/pfd-resources-and-quick-references/procedures/Neonatal_Resuscitation.html",
    "/pfd-resources-and-quick-references/procedures/Spinal_Motion_Restriction.html",
    "/pfd-resources-and-quick-references/procedures/Surgical_Airway.html",
    "/pfd-resources-and-quick-references/procedures/Taser_Barb_Removal.html",
    "/pfd-resources-and-quick-references/procedures/Tourniquet_Application.html",
    "/pfd-resources-and-quick-references/procedures/Transcutaneous_Pacing.html",
    "/pfd-resources-and-quick-references/procedures/Vaccination.html",
    "/pfd-resources-and-quick-references/protocols/00 - Master Protocol Tracker.html",
    "/pfd-resources-and-quick-references/protocols/administrative/01_ALS_Release_to_BLS_PROC.html",
    "/pfd-resources-and-quick-references/protocols/administrative/01_Abuse_Recognition_and_Mandated_Reporting_PROC.html",
    "/pfd-resources-and-quick-references/protocols/administrative/01_Behavioral_Health_Transportation_Decision_PROC.html",
    "/pfd-resources-and-quick-references/protocols/administrative/01_Communications_PROC.html",
    "/pfd-resources-and-quick-references/protocols/administrative/01_Death_Criteria_for_Withholding_Resuscitation_PROC.html",
    "/pfd-resources-and-quick-references/protocols/administrative/01_Helicopter_EMS_HEMS_PROC.html",
    "/pfd-resources-and-quick-references/protocols/administrative/01_Infant_Abandonment_PROC.html",
    "/pfd-resources-and-quick-references/protocols/administrative/01_Patient_Refusal_of_Treatment_Transport_PROC.html",
    "/pfd-resources-and-quick-references/protocols/administrative/01_Patient_Restraint_PROC.html",
    "/pfd-resources-and-quick-references/protocols/administrative/01_STEMI_Field_Triage_PROC.html",
    "/pfd-resources-and-quick-references/protocols/administrative/01_Safe_Transport_of_Pediatric_Patients_PROC.html",
    "/pfd-resources-and-quick-references/protocols/administrative/01_Stroke_Field_Triage_PROC.html",
    "/pfd-resources-and-quick-references/protocols/administrative/01_Transportation_and_Destination_Determination_PROC.html",
    "/pfd-resources-and-quick-references/protocols/administrative/01_Trauma_Field_Triage_PROC.html",
    "/pfd-resources-and-quick-references/protocols/cardiac/04_Asystole_and_Pulseless_Electrical_Activity_PROC.html",
    "/pfd-resources-and-quick-references/protocols/cardiac/04_Bradycardia_PROC.html",
    "/pfd-resources-and-quick-references/protocols/cardiac/04_Cardiac_Arrest_Non_Traumatic_PROC.html",
    "/pfd-resources-and-quick-references/protocols/cardiac/04_Cardiac_Arrest_Traumatic_PROC.html",
    "/pfd-resources-and-quick-references/protocols/cardiac/04_Chest_Pain_ACS_PROC.html",
    "/pfd-resources-and-quick-references/protocols/cardiac/04_Hypertensive_Crisis_PROC.html",
    "/pfd-resources-and-quick-references/protocols/cardiac/04_Post_Resuscitation_Care_PROC.html",
    "/pfd-resources-and-quick-references/protocols/cardiac/04_Supraventricular_Tachycardia_PROC.html",
    "/pfd-resources-and-quick-references/protocols/cardiac/04_V_Fib_Pulseless_V_Tach_PROC.html",
    "/pfd-resources-and-quick-references/protocols/cardiac/04b_Aortic_Dissection_AAA_PROC.html",
    "/pfd-resources-and-quick-references/protocols/front-matter/00 - AI Formatting Guidelines.html",
    "/pfd-resources-and-quick-references/protocols/front-matter/00 - Introduction.html",
    "/pfd-resources-and-quick-references/protocols/front-matter/01 - How to Read the Protocols.html",
    "/pfd-resources-and-quick-references/protocols/front-matter/Universal Patient Care.html",
    "/pfd-resources-and-quick-references/protocols/general/02_Behavioral_Patient_Restraint_PROC.html",
    "/pfd-resources-and-quick-references/protocols/general/02_Cold_Exposure_PROC.html",
    "/pfd-resources-and-quick-references/protocols/general/02_Diving_and_Drowning_Emergencies_PROC.html",
    "/pfd-resources-and-quick-references/protocols/general/02_Heat_Exposure_PROC.html",
    "/pfd-resources-and-quick-references/protocols/general/02_Pain_Control_PROC.html",
    "/pfd-resources-and-quick-references/protocols/general/02_Sedation_Assisted_Non_Paralytic_PROC.html",
    "/pfd-resources-and-quick-references/protocols/medical/07_Allergic_Reaction_Anaphylaxis_PROC.html",
    "/pfd-resources-and-quick-references/protocols/medical/07_Hypotension_Shock_Non_Trauma_PROC.html",
    "/pfd-resources-and-quick-references/protocols/medical/07_OB_Emergencies_PROC.html",
    "/pfd-resources-and-quick-references/protocols/medical/07_Sepsis_PROC.html",
    "/pfd-resources-and-quick-references/protocols/neurologic/05_Hypoglycemia_Hyperglycemia_PROC.html",
    "/pfd-resources-and-quick-references/protocols/neurologic/05_Seizure_PROC.html",
    "/pfd-resources-and-quick-references/protocols/neurologic/05_Stroke_TIA_PROC.html",
    "/pfd-resources-and-quick-references/protocols/respiratory/03_Airway_Inhalation_Irritants_PROC.html",
    "/pfd-resources-and-quick-references/protocols/respiratory/03_Asthma_COPD_Reactive_Airway_PROC.html",
    "/pfd-resources-and-quick-references/protocols/respiratory/03_Pediatric_Stridor_PROC.html",
    "/pfd-resources-and-quick-references/protocols/respiratory/03_Pneumothorax_PROC.html",
    "/pfd-resources-and-quick-references/protocols/respiratory/03_Pulmonary_Edema_Congestion_PROC.html",
    "/pfd-resources-and-quick-references/protocols/respiratory/03_Respiratory_Arrest_PROC.html",
    "/pfd-resources-and-quick-references/protocols/respiratory/03_Respiratory_Distress_PROC.html",
    "/pfd-resources-and-quick-references/protocols/respiratory/03_Smoke_Inhalation_PROC.html",
    "/pfd-resources-and-quick-references/protocols/respiratory/03_Upper_Airway_Obstruction_PROC.html",
    "/pfd-resources-and-quick-references/protocols/toxicology/06_Nausea_Vomiting_PROC.html",
    "/pfd-resources-and-quick-references/protocols/toxicology/06_Nerve_Agents_PROC.html",
    "/pfd-resources-and-quick-references/protocols/toxicology/06_Overdose_Poisoning_PROC.html",
    "/pfd-resources-and-quick-references/protocols/trauma/09_Burns_Thermal_PROC.html",
    "/pfd-resources-and-quick-references/protocols/trauma/09_Crush_Syndrome_PROC.html",
    "/pfd-resources-and-quick-references/protocols/trauma/09_Electrical_Injuries_PROC.html",
    "/pfd-resources-and-quick-references/protocols/trauma/09_Hemorrhage_Control_PROC.html",
    "/pfd-resources-and-quick-references/protocols/trauma/09_Lightning_Injuries_PROC.html",
    "/pfd-resources-and-quick-references/protocols/trauma/09_Trauma_PROC.html",
    "/pfd-resources-and-quick-references/sops/emergency-operations/EO-10-Staffing-and-Equipment-Response-202406130909086447.html",
    "/pfd-resources-and-quick-references/sops/emergency-operations/EO-100-Incident-Management-System.html",
    "/pfd-resources-and-quick-references/sops/emergency-operations/EO-110-Elevator-Emergencies.html",
    "/pfd-resources-and-quick-references/sops/emergency-operations/EO-120-Lock-Out-Tag-Out.html",
    "/pfd-resources-and-quick-references/sops/emergency-operations/EO-1300-Motor-Vehicle-Fires.html",
    "/pfd-resources-and-quick-references/sops/emergency-operations/EO-200-Emergency-Operations-in-Atmosphere-Immediately-Dangerous-to-Life-and-Health.html",
    "/pfd-resources-and-quick-references/sops/emergency-operations/EO-300-Safe-Apparatus-Positioning.html",
    "/pfd-resources-and-quick-references/sops/emergency-operations/EO-400-Ventilation.html",
    "/pfd-resources-and-quick-references/sops/emergency-operations/EO-500-Radio-Communications.html",
    "/pfd-resources-and-quick-references/sops/emergency-operations/EO-510-Paging-Day-Night-Switch.html",
    "/pfd-resources-and-quick-references/sops/emergency-operations/EO-600-First-to-Arrive-Duties.html",
    "/pfd-resources-and-quick-references/sops/emergency-operations/EO-700-Engine-Company-Operations.html",
    "/pfd-resources-and-quick-references/sops/emergency-operations/EO-800-Ladder-Company-Operations.html",
    "/pfd-resources-and-quick-references/sops/emergency-operations/EO-900-Emergency-Incident-Rehabilitation.html",
    "/pfd-resources-and-quick-references/sops/ems/EMS-100-General-EMS-Guidelines.html",
    "/pfd-resources-and-quick-references/sops/ems/EMS-1000-ALS-Engine-Response.html",
    "/pfd-resources-and-quick-references/sops/ems/EMS-1100-QA-QI.html",
    "/pfd-resources-and-quick-references/sops/ems/EMS-1200-Patient-Transport.html",
    "/pfd-resources-and-quick-references/sops/ems/EMS-1300-EMS-Certifications.html",
    "/pfd-resources-and-quick-references/sops/ems/EMS-1400-Minimum-Acceptable-Training.html",
    "/pfd-resources-and-quick-references/sops/ems/EMS-1500-Regional-Protocol-Testing.html",
    "/pfd-resources-and-quick-references/sops/ems/EMS-1600-EMS-Routine-Transport.html",
    "/pfd-resources-and-quick-references/sops/ems/EMS-1700-Mandatory-Reporting.html",
    "/pfd-resources-and-quick-references/sops/ems/EMS-1800-Release-of-Confidential-Information.html",
    "/pfd-resources-and-quick-references/sops/ems/EMS-1900-Incident-Infection-Control.html",
    "/pfd-resources-and-quick-references/sops/ems/EMS-191-Hemostatic-Agents.html",
    "/pfd-resources-and-quick-references/sops/ems/EMS-200-Infection-Control-Plan-Policy.html",
    "/pfd-resources-and-quick-references/sops/ems/EMS-2000-Medication-Management-and-Pharmacy.html",
    "/pfd-resources-and-quick-references/sops/ems/EMS-2100-Controlled-Substances.html",
    "/pfd-resources-and-quick-references/sops/ems/EMS-300-EMS-Supplies-and-Equipment.html",
    "/pfd-resources-and-quick-references/sops/ems/EMS-400-Advanced-Life-Support-Preceptorship.html",
    "/pfd-resources-and-quick-references/sops/ems/EMS-500-Downgrading-ALS-Calls-to-BLS-Calls.html",
    "/pfd-resources-and-quick-references/sops/ems/EMS-600-EMS-Do-Not-Resuscitate.html",
    "/pfd-resources-and-quick-references/sops/ems/EMS-700-Failure-to-Comply-with-Regional-Protocols.html",
    "/pfd-resources-and-quick-references/sops/ems/EMS-800-BLS-Preceptorship-Program.html",
    "/pfd-resources-and-quick-references/sops/ems/EMS-900-Drug-Box-Procedures.html",
    "/pfd-resources-and-quick-references/sops/equipment-and-apparatus/EA-100-Hose-Testing-and-Maintenance.html",
    "/pfd-resources-and-quick-references/sops/equipment-and-apparatus/EA-1000-Dry-Hydrants.html",
    "/pfd-resources-and-quick-references/sops/equipment-and-apparatus/EA-200-Pump-Testing.html",
    "/pfd-resources-and-quick-references/sops/equipment-and-apparatus/EA-300-Map-Books.html",
    "/pfd-resources-and-quick-references/sops/equipment-and-apparatus/EA-400-Apparatus-Inspection-and-Maintenance.html",
    "/pfd-resources-and-quick-references/sops/equipment-and-apparatus/EA-500-PPE-and-Equipment.html",
    "/pfd-resources-and-quick-references/sops/equipment-and-apparatus/EA-600-Portable-Radios.html",
    "/pfd-resources-and-quick-references/sops/equipment-and-apparatus/EA-700-Ladder-Maintenance.html",
    "/pfd-resources-and-quick-references/sops/equipment-and-apparatus/EA-800-PPE-Inspections.html",
    "/pfd-resources-and-quick-references/sops/equipment-and-apparatus/EA-911-Reporting-of-Off-Site-Training.html",
    "/pfd-resources-and-quick-references/sops/general-administration/GA-100-Chain-of-Command.html",
    "/pfd-resources-and-quick-references/sops/general-administration/GA-1000-Hiring-Process.html",
    "/pfd-resources-and-quick-references/sops/general-administration/GA-1100-Take-Home-Vehicle-Assignment.html",
    "/pfd-resources-and-quick-references/sops/general-administration/GA-1200-Incident-Reporting-202306231515040783.html",
    "/pfd-resources-and-quick-references/sops/general-administration/GA-1210-Records-Retention.html",
    "/pfd-resources-and-quick-references/sops/general-administration/GA-1300-Annual-and-Bereavement-Leave.html",
    "/pfd-resources-and-quick-references/sops/general-administration/GA-1400-Pre-Incident-Planning.html",
    "/pfd-resources-and-quick-references/sops/general-administration/GA-1500-Software-Copyright-Violation.html",
    "/pfd-resources-and-quick-references/sops/general-administration/GA-1600-Driving-Emergency-Vehicles.html",
    "/pfd-resources-and-quick-references/sops/general-administration/GA-1700-Fire-and-EMS-Preceptor.html",
    "/pfd-resources-and-quick-references/sops/general-administration/GA-1800-Promotional-Process-for-Battalion-Chief-202407090842463106.html",
    "/pfd-resources-and-quick-references/sops/general-administration/GA-1900-Promotional-Process-for-Fire-Lieutenant-202407120905160146.html",
    "/pfd-resources-and-quick-references/sops/general-administration/GA-1910-Promotional-Process-for-Master-Firefighter-202407120905411525.html",
    "/pfd-resources-and-quick-references/sops/general-administration/GA-1920-Acting-Officer-Program.html",
    "/pfd-resources-and-quick-references/sops/general-administration/GA-200-Code-of-Ethics.html",
    "/pfd-resources-and-quick-references/sops/general-administration/GA-2000-Revenue-Recovery-202205120923573966.html",
    "/pfd-resources-and-quick-references/sops/general-administration/GA-210-Non-Discrimination.html",
    "/pfd-resources-and-quick-references/sops/general-administration/GA-2100-Compensatory-Time-Policy-202205120924154260.html",
    "/pfd-resources-and-quick-references/sops/general-administration/GA-2200-Family-Medical-Leave-Act-FMLA-202205120924326282.html",
    "/pfd-resources-and-quick-references/sops/general-administration/GA-2300-Work-Status-Options-for-Pregnant-Members-202205120924526749.html",
    "/pfd-resources-and-quick-references/sops/general-administration/GA-2400-Applicant-Guidelines-and-Disqualifiers.html",
    "/pfd-resources-and-quick-references/sops/general-administration/GA-2500-Authorized-Use-of-Utility-1-202205120925143466.html",
    "/pfd-resources-and-quick-references/sops/general-administration/GA-2600-Football-Game-Standbys-202212071036091388.html",
    "/pfd-resources-and-quick-references/sops/general-administration/GA-2700-Awards-and-Recognition.html",
    "/pfd-resources-and-quick-references/sops/general-administration/GA-2800-Overtime-202406130906401118.html",
    "/pfd-resources-and-quick-references/sops/general-administration/GA-2900-Fire-Investigations.html",
    "/pfd-resources-and-quick-references/sops/general-administration/GA-400-Tobacco-Product-Use.html",
    "/pfd-resources-and-quick-references/sops/general-administration/GA-500-Energy-Conservation.html",
    "/pfd-resources-and-quick-references/sops/general-administration/GA-600-Shift-Trades.html",
    "/pfd-resources-and-quick-references/sops/general-administration/GA-700-Uniforms-rev2023-202310190745013246.html",
    "/pfd-resources-and-quick-references/sops/general-administration/GA-900-Training-and-Weather-Conditions.html",
    "/pfd-resources-and-quick-references/sops/general-administration/GA-910-Training-Administration.html",
    "/pfd-resources-and-quick-references/sops/general-administration/GA-911-Reporting-of-Off-Site-Training.html",
    "/pfd-resources-and-quick-references/sops/public-relations/PR-100-SAFE-House-Policy.html",
    "/pfd-resources-and-quick-references/sops/public-relations/PR-200-Ride-Along-Program.html",
    "/pfd-resources-and-quick-references/sops/public-relations/PR-300-Station-Tours.html",
    "/pfd-resources-and-quick-references/sops/public-relations/PR-400-Apparatus-Displays-Standbys.html",
    "/pfd-resources-and-quick-references/sops/safety-and-health/SH-100-Hearing-Conservation.html",
    "/pfd-resources-and-quick-references/sops/safety-and-health/SH-200-Respiratory-Protection-Program-202103251459187916.html",
    "/pfd-resources-and-quick-references/sops/safety-and-health/SH-300-Station-Conduct-and-Safety.html",
    "/pfd-resources-and-quick-references/sops/safety-and-health/SH-400-Critical-Incident-Stress-Management.html",
    "/pfd-resources-and-quick-references/sops/safety-and-health/SH-500-Facility-Safety-Checks.html",
    "/pfd-resources-and-quick-references/sops/safety-and-health/SH-600-Bedbugs-Prevention-Detection-Treatment.html",
    "/pfd-resources-and-quick-references/sops/special-operations/SO-100-Confined-Space-Rescue.html",
    "/pfd-resources-and-quick-references/sops/special-operations/SO-200-Hazardous-Materials-Incidents.html",
    "/pfd-resources-and-quick-references/sops/special-operations/SO-300-Elevator-Entrapment-Rescues.html",
    "/pfd-resources-and-quick-references/sops/special-operations/SO-400-Structural-Collapse-Search-and-Rescue.html",
    "/pfd-resources-and-quick-references/sops/special-operations/SO-500-Helicopter-Assistance.html",
    "/pfd-resources-and-quick-references/sops/special-operations/SO-600-Severe-Weather-Vehicle-Operations.html",
    "/pfd-resources-and-quick-references/sops/special-operations/SO-700-Explosive-Device-Incidents.html",
    "/pfd-resources-and-quick-references/sops/special-operations/SO-800-Natural-Gas-Emergencies.html",
    "/pfd-resources-and-quick-references/sops/special-operations/so-1000-boat-operations.html",
    "/pfd-resources-and-quick-references/sops/special-operations/so-1100-extreme-weather-emergencies-and-natural-disaster-call-back-policy.html",
    "/pfd-resources-and-quick-references/sops/special-operations/so-1200-suas-operations.html",
    "/pfd-resources-and-quick-references/sops/special-operations/so-1300-rescue-task-force-administration.html",
    "/pfd-resources-and-quick-references/sops/special-operations/so-900-carbon-monoxide-incident-operations.html"
];

// Install: download and cache every page
self.addEventListener("install", event => {
    console.log("[SW] Installing — caching {PRECACHE_URLS.length} pages...");
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                // Cache in small batches to avoid overwhelming the browser
                const batchSize = 10;
                const cacheInBatches = async () => {
                    for (let i = 0; i < PRECACHE_URLS.length; i += batchSize) {
                        const batch = PRECACHE_URLS.slice(i, i + batchSize);
                        await Promise.all(
                            batch.map(url =>
                                cache.add(url).catch(err =>
                                    console.warn("[SW] Failed to cache:", url, err)
                                )
                            )
                        );
                        console.log(`[SW] Cached ${Math.min(i + batchSize, PRECACHE_URLS.length)}/${PRECACHE_URLS.length} pages`);
                    }
                };
                return cacheInBatches();
            })
            .then(() => self.skipWaiting())
    );
});

// Activate: clean up old caches
self.addEventListener("activate", event => {
    console.log("[SW] Activating — cleaning old caches");
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames
                    .filter(name => name !== CACHE_NAME)
                    .map(name => {
                        console.log("[SW] Deleting old cache:", name);
                        return caches.delete(name);
                    })
            );
        }).then(() => self.clients.claim())
    );
});

// Fetch: cache-first strategy — serve from cache, fall back to network
self.addEventListener("fetch", event => {
    // Only handle GET requests for same-origin resources
    if (event.request.method !== "GET") return;
    
    const url = new URL(event.request.url);
    
    // Only cache same-origin HTML pages and assets
    if (url.origin !== self.location.origin) return;
    
    event.respondWith(
        caches.match(event.request).then(cachedResponse => {
            if (cachedResponse) {
                return cachedResponse;
            }
            // Not in cache — fetch from network and cache for next time
            return fetch(event.request).then(response => {
                if (response && response.status === 200) {
                    const responseToCache = response.clone();
                    caches.open(CACHE_NAME).then(cache => {
                        cache.put(event.request, responseToCache);
                    });
                }
                return response;
            }).catch(() => {
                // Offline and not cached — return the homepage
                return caches.match("/pfd-resources-and-quick-references/index.html");
            });
        })
    );
});

console.log("[SW] Poquoson Fire & Rescue — 217 pages ready for offline use");
