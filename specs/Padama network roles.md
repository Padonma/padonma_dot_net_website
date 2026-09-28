# Padama Network Roles and Coordination Specification

Status: concept specification

Scope: network roles, evidence, coordination, finance interfaces, quality assurance, logistics, and insurance

Terminology: the project and protocol are referred to as **Padama** in this document. The wider project may also be known as Padonma.

## 1. Purpose and non-goals

Padama is an open-source coordination and evidence network for the lotus-fiber textile industry. Its purpose is to make it easier for independent people and organizations to specialize, trade, coordinate production, demonstrate quality and provenance, and offer related services.

Padama should publish software and open-hardware designs freely enough that a self-sustaining marketplace can emerge around them. Economic activity is performed by independent artisans, cooperatives, nonprofits, companies, and service providers. Padama provides shared protocols and records; it does not own the whole value chain.

### 1.1 Goals

- Define interoperable identities, orders, products, milestones, quality evidence, custody events, and reputation records.
- Reduce coordination and verification costs without requiring a single central operator.
- Make small-scale rural production legible to buyers, financiers, logistics providers, and insurers while preserving meaningful participant choice.
- Let independent providers compete in training, coordination, quality assurance, appeals, finance, insurance, transport, and other services.
- Support low-cost Android phones and intermittent connectivity.
- Keep the core implementation open source and key equipment designs open hardware.

### 1.2 Non-goals

Padama is not, by itself:

- the sole employer, purchaser, marketplace operator, production coordinator, lender, guarantor, insurer, payment processor, carrier, certification authority, or dispute tribunal;
- a promise that every participant or product is trustworthy;
- a substitute for contracts, applicable law, regulated financial services, licensed insurance, customs documentation, or carrier terms;
- a cryptocurrency or payment system; existing payment providers move money;
- a requirement to use a blockchain or an NFT; or
- a claim that automated image analysis can replace buyer-defined acceptance, human judgment, or appeals.

This document describes a technical and operating model, not regulatory, financial, insurance, or legal advice.

## 2. Design principles

1. **Protocol before platform.** Define portable records and verifiable events so that multiple applications and service providers can interoperate.
2. **Plural providers.** Avoid encoding one mandatory coordinator, certifier, financier, carrier, insurer, or dispute resolver.
3. **Evidence, not omniscience.** A signed record shows who asserted what, when, and with which evidence. It does not make the assertion true by itself.
4. **Buyer-defined acceptance.** Buyers publish measurable acceptance criteria with an order. QA services evaluate evidence against those criteria.
5. **Human appeal.** Automated assessments must be reviewable, explainable at an operational level, and contestable.
6. **Progressive trust.** New participants can begin with small orders and limited exposure; verified performance can expand available work and financing.
7. **Offline-tolerant and accessible.** Essential capture should work on common Android devices, queue locally, and synchronize when connectivity returns.
8. **Data minimization and consent.** Public provenance should not expose unnecessary personal data, precise home locations, or commercially sensitive terms.
9. **Technology neutrality.** Stable identifiers and signed events are foundational. Blockchain anchoring is optional and should be used only where it adds verifiable value.
10. **No unsafe capital assumptions.** A productive asset does not automatically justify individual debt. Capital structure must match utilization, ability to repay, and order flow.

## 3. Entities and roles

One participant may perform multiple roles, and roles may be performed by an individual, cooperative, nonprofit, company, or other lawful entity. Role claims should state the issuer and supporting evidence rather than implying universal accreditation.

### 3.1 Production roles

- **Lotus-fiber preparer or thread spinner:** prepares fiber and spins thread to a stated specification.
- **Weaver:** turns thread into fabric or a garment component and records input and output evidence.
- **Garment maker or finisher:** cuts, sews, washes, presses, repairs, or finishes a product.
- **Hand-woven QR-code band specialist:** weaves a scannable band for another producer's garment. Entry capital is expected to be minimal beyond thread, instructional media, and free pattern-generation software.
- **Local loom builder:** uses open-source frame-loom designs and locally available wood to manufacture, repair, or adapt looms.
- **Shared-facility operator:** owns or stewards communal looms, tools, workspace, or calibration aids and rents time or access under published terms.

**Planning assumptions, not validated facts:** an early labor model may require roughly **20 thread spinners per weaver**. A simple locally built frame loom may cost roughly **US$100**. Both figures require field validation by geography, wage level, material, design, throughput, and date. Loom demand may be intermittent, making shared ownership more suitable than one loan per artisan.

### 3.2 Coordination and market roles

- **Buyer:** posts an order and acceptance criteria, funds it through an external payment provider, accepts or disputes delivery, and may appoint agents.
- **Production coordinator or steward:** decomposes orders, matches participants, schedules work, monitors milestones, and assists with exceptions without becoming the protocol's mandatory intermediary.
- **Aggregator or hub operator:** consolidates inputs or outputs, provides storage, records handoffs, and may perform finishing or packing.
- **Trainer:** teaches fiber preparation, spinning, weaving, garment production, QR-band weaving, evidence capture, QA, safety, or business practices.
- **Materials supplier:** sells or provides inputs, possibly on disclosed trade-credit terms tied to an order.
- **Transporter or courier:** moves goods between custody points and signs pickup, handoff, condition, and delivery events.

### 3.3 Assurance and risk roles

- **Automated QA service:** evaluates submitted images, measurements, and metadata against declared criteria and returns scores, flags, confidence, and model/version information.
- **Independent QA reviewer:** provides paid or sponsored human inspection, second opinions, or certification under clearly named rules.
- **QA appeals specialist:** reviews contested automated or human findings while remaining organizationally separable from the original assessor where practical.
- **Dispute resolver:** mediates or adjudicates commercial disputes under terms accepted by the parties.
- **Identity or credential provider:** verifies limited identity or capability claims at an assurance level appropriate to the transaction.
- **Financier or guarantee provider:** advances capital, purchases receivables, provides trade credit, or guarantees performance under its own lawful terms.
- **Licensed insurer or broker:** quotes, binds, underwrites, administers, or distributes coverage where authorized. Padama does not assume the insured risk.
- **Data/model auditor:** examines QA models, error patterns, event integrity, or service-provider claims.

## 4. Core objects and records

All records should have a stable identifier, schema version, issuer, creation time, signature or equivalent authentication, visibility policy, and links to superseded or related records. Corrections should be appended rather than silently rewriting history.

### 4.1 Participant and role profile

Contains participant identifier, optional verified identity references, declared roles, service area, capabilities, equipment access, credentials, consent settings, and aggregated performance history. Public views should use pseudonymous or coarse location data where possible.

### 4.2 Order

Contains buyer, product specification, quantities, due dates, destination, price and currency, externally managed payment terms, acceptance criteria, evidence requirements, permitted substitutions, dispute route, cancellation rules, and financing eligibility. An order must distinguish a buyer commitment from an expression of interest.

### 4.3 Work package and milestone

Represents a bounded unit of spinning, weaving, QR-band production, assembly, QA, aggregation, or transport. It records assigned party, inputs, expected output, deadline, dependencies, evidence, status, and acceptance or rejection reason.

### 4.4 Asset and facility record

Describes a loom, shared workspace, tool, or other productive asset: design/version, builder, ownership or stewardship, location at appropriate granularity, availability, usage charges, maintenance, repair, and calibration history.

### 4.5 Product passport

Each garment receives a stable product identifier linked from a woven or attached QR code. The passport references material and transformation events, QA results, custody history, repair or care information, and selected provenance claims. It must separate private commercial data from buyer-facing or public provenance.

The stable product identifier and signed event chain are sufficient for most uses. An NFT is optional and should be introduced only if transferable on-chain ownership is an actual requirement, not as a synonym for authenticity.

### 4.6 Evidence bundle and QA assessment

An evidence bundle references photographs, weight or dimensional measurements, capture metadata, operator, device/application version, and a tamper-evident digest. A QA assessment references the exact evidence, criteria, method or model version, results, confidence, limitations, reviewer identity, and appeal status.

### 4.7 Custody and condition event

Records product, sender, recipient, time, coarse or consented location, package identifier, carrier or transport mode, observed condition, supporting images or documents, and both parties' acknowledgements where feasible.

### 4.8 Finance, payment, and insurance references

Padama records only the minimum references needed to connect an order or milestone to an offer, external payment, guarantee, policy, premium, coverage period, claim, or payout. Sensitive account data remains with the relevant regulated or contracted provider. A Padama status such as `payment-released` is evidence received from an external provider, not movement of funds by Padama.

### 4.9 Reputation statement

Reputation is a collection of attributable statements and computed summaries, not a universal score. It should preserve context such as role, order size, criteria, recency, disputes, and sample size, and provide a correction and appeal path.

## 5. Lifecycle and event flow

A representative order proceeds as follows:

1. A buyer publishes an order with product specification, quantity, price, timing, QA thresholds, evidence, delivery terms, and dispute route.
2. A coordinator, cooperative, or producers propose a production plan. The plan allocates spinning, weaving, QR-band, finishing, QA, aggregation, and transport work packages.
3. Participants accept work packages. Any financier, supplier credit, guarantee, facility rental, or preorder funding is separately offered and accepted against the verified order.
4. Inputs and loom access are issued or purchased. Relevant custody, debt, rental, and milestone terms are recorded by reference.
5. Producers submit milestone evidence. Existing payment providers may release advances or milestone payments when the contracted conditions are met.
6. The Android web app captures photographs and measurements. Automated QA returns results; flagged or appealed cases go to an independent reviewer.
7. Accepted components are assembled or aggregated. A stable garment identifier and QR-linked product passport are created.
8. Custody events record movement from the rural producer—for example, in northeast Myanmar/Burma—to a motorcycle courier, city hub, international carrier such as DHL, and buyer in Paris.
9. Delivery, condition, acceptance, external payment status, and any claim or dispute outcomes are recorded.
10. Participants receive context-specific reputation statements. Sensitive evidence follows the retention and deletion policy agreed for the order.

Events may be batched and cryptographically anchored to a blockchain. The operational record should remain usable without requiring every participant to hold cryptocurrency or transact on-chain.

## 6. Distributed QA boundary

### 6.1 Required capability

Padama should provide a free and open-source web application usable on Android phones. It should let participants photograph fabric or garments, including a backlit view where the applicable procedure calls for one, record weight and other required evidence, review the submission, and synchronize it.

Image recognition or other automated methods may estimate or flag:

- slubs and other visible irregularities;
- thread count;
- transparency;
- thread-thickness regularity;
- weave tightness and regularity; and
- visible defects.

The service returns evidence-linked observations, confidence, and limitations. The buyer's published criteria determine acceptance; an AI output is not itself a universal grade or certification.

### 6.2 Deliberate boundary

Detailed capture geometry, lighting, backlight apparatus, reference targets, device calibration, scale calibration, tolerances, and model-validation procedures are specified elsewhere. This document requires only that procedures be versioned, feasible on target devices, resistant to common capture errors, and able to reveal when evidence is inadequate.

### 6.3 Decentralization and appeals

- Multiple automated and human QA providers may compete.
- A provider must disclose criteria version, method/model version, confidence, and conflicts of interest.
- Rejection must include a reason code and access to the underlying evidence allowed by the order.
- A participant may request paid, buyer-funded, cooperative-funded, or otherwise sponsored human review according to disclosed terms.
- Appeals preserve the original decision and append the review result.
- Pilot evaluation must measure false acceptance and false rejection across devices, lighting conditions, materials, and participant groups.

## 7. Financing services and capital stack

Padama standardizes the evidence needed for finance but does not lend, take deposits, transmit money, or imply that a protocol record makes an offer lawful or suitable.

### 7.1 Distributed order-linked model

- Buyers post sufficiently firm orders rather than vague demand forecasts.
- Independent financiers may advance against verified orders or accepted milestones.
- Materials suppliers may offer disclosed trade credit.
- Communal entities may buy looms and rent time rather than requiring each artisan to borrow for an underused asset.
- Guarantors or licensed insurers may cover defined risks.
- Existing payment providers release funds according to agreed instructions and verified milestones.
- Padama supplies standardized orders, identities or credentials, milestones, QA, delivery evidence, and contextual reputation.

### 7.2 Suggested capital stack

From most risk-absorbing or patient to most repayable:

1. grants, donations, or recoverable seed capital for pilot and communal looms;
2. affordable member contributions that do not exclude the poorest participants;
3. transparent usage charges reserved for operation, maintenance, and replacement;
4. buyer preorders or purchase-order advances;
5. supplier input credit tied to a real production plan;
6. independent revolving funds, first-loss reserves, or guarantees; and
7. an optional, openly governed voluntary transaction assessment for a resilience or guarantee fund.

The stack should state who absorbs first loss, who controls reserves, how fees are set, how surpluses are used, and how a participant exits.

### 7.3 Debt safeguards

Individual microcredit is not presumed to be the best way to finance an approximately US$100 shared asset. Research across randomized evaluations finds modest average effects and heterogeneous outcomes rather than a universal transformation. Loans, where used, should have transparent total pricing, affordable and flexible repayment, no coercive group liability, clear hardship procedures, and a plausible repayment source tied to productive use or real orders. The poorest participants may be better served by grants, subsidies, shared assets, or paid training. The pilot must monitor multiple borrowing and over-indebtedness without building an invasive universal credit score.

## 8. Insurance and logistics extension

Padama provides evidence and event records. Licensed insurers or other authorized risk carriers underwrite coverage, contracted administrators handle claims, and existing payment services make premium and claim payments.

### 8.1 Quoting inputs

With appropriate consent, an insurer may quote from:

- participant identity or assurance level and relevant history;
- product QA evidence, weight, declared value, and fragility;
- origin, destination, route, carrier, and expected transit time;
- packaging specification and evidence;
- custody plan and required scan points; and
- prior delivery and claim history at a proportionate level of detail.

Insurers should receive the record version used for a quote so later corrections do not silently alter the basis of coverage.

### 8.2 Policy and claim flow

1. One or more providers quote coverage against a shipment record.
2. The buyer, seller, coordinator, or other eligible party accepts coverage with the provider.
3. Padama stores the policy reference, covered product/shipment IDs, coverage window, required evidence, and provider-signed status.
4. Custody scans, carrier events, delivery evidence, and damage evidence support a claim.
5. The licensed provider decides the claim under the policy; Padama records attributable decisions and external payout status.

Multiple underwriters may share a defined risk through a lead/follow or subscription structure analogous in shape to the Lloyd's market. Padama must not present that analogy as authorization to form an unlicensed risk pool.

### 8.3 Technology choices

- Signed events and stable identifiers are the default.
- Blockchain anchoring may add independent timestamping and tamper evidence for selected event digests.
- On-chain smart contracts may support a provider's parametric product, but should not be required for ordinary custody or damage coverage.
- An NFT is used only when transferable on-chain title is explicitly required.

## 9. Governance, trust, and disputes

### 9.1 Governance scope

Open governance maintains schemas, conformance tests, reference software, open-hardware designs, security disclosures, and change procedures. It does not decide every commercial dispute or confer blanket legitimacy on providers.

Protocol changes should use public proposals, documented rationale, review periods, versioning, and migration paths. Representation should include producers, especially women and rural participants, as well as buyers, coordinators, technical contributors, and independent assurance providers. Financial sponsorship and conflicts must be disclosed.

### 9.2 Trust model

- Every material claim is attributable to its issuer.
- Assurance levels distinguish self-assertion, peer attestation, documentary verification, observation, and independent audit.
- Endorsements expire or carry observation dates.
- Service-provider directories are open to multiple qualifying providers and disclose listing rules.
- No single reputation number follows a person without context.
- Sensitive data access is purpose-limited, logged, revocable where feasible, and retained only as long as needed.

### 9.3 Dispute model

Orders specify governing commercial terms, evidence rules, response times, and a chosen dispute path before work begins. The system should support negotiation, mediation, and third-party determination without pretending that protocol governance replaces courts or statutory rights. A resolver records the decision, reasons, evidence references, conflicts, and appeal route. Retaliatory ratings and exclusion following a good-faith appeal should be detectable and reviewable.

## 10. Precedent comparison and lessons

These precedents are from non-lotus sectors unless expressly stated otherwise. They demonstrate particular techniques, not an end-to-end Padama-equivalent system, and must never be described as lotus-fiber programs.

| Precedent | Demonstrated technique | Padama lesson | Important difference |
| --- | --- | --- | --- |
| [BRAC/Aarong and the Ayesha Abed Foundation](https://www.brac.net/solutions/social-enterprise/aarong/) | A BRAC social enterprise using production centers and sub-centers to connect rural artisans to markets, provide services, and support timely payment | Adapt order distribution, input support, local hubs, quality control, and producer services into interoperable roles | Aarong is centrally managed; it is not a government program or a distributed protocol |
| [BRAC interview describing the hub-and-spoke model](https://www.brac.net/stay-informed/news/aarong-bracs-social-enterprises-and-life-an-interview-with-tamara-hasan-abed-senior-director-brac/) | Main centers receive orders and prepare/distribute work and raw materials; Aarong historically paid on delivery and assumed inventory/market risk | Finance should follow real orders; payment on accepted delivery, materials on credit, collateral-free working-capital loans where suitable, occasional advances or emergency loans, year-round order smoothing, surplus reinvestment, and risk-bearing intermediaries may protect artisans from retail-sale delay | Padama separates these functions among voluntary providers rather than assigning them all to one enterprise |
| [India's SFURTI cluster program](https://sfurti.msme.gov.in/) and Common Facility Centres | Shared facilities, cluster institutions, skill development, and common production or processing capacity | Pool intermittently used looms, tools, training, maintenance, and QA infrastructure | Government-supported cluster implementation differs from an open, cross-provider network |
| Chanderi producer-company experience | Producer ownership and aggregation can improve collective market access and bargaining | Test producer-owned coordination, shared services, and representation in governance | Results depend on local institutions and should not be generalized without field study |
| [Trama Textiles](https://tramatextiles.org/) in Guatemala | A producer-facing weaving cooperative connects artisans, products, and markets | Preserve producer voice, transparent allocation, and collective services | Cooperative retail/export operations are more integrated than the Padama protocol layer |
| [WomenWeave](https://womenweave.org/) in India | Training, livelihood support, design/market links, and handloom ecosystem development | Treat training and capability building as sustained services, not a one-time app onboarding | Its organizational model and textile context differ from lotus fiber |
| [UN International Trade Centre Ethical Fashion Initiative](https://www.intracen.org/our-work/projects/ethical-fashion-initiative) | Market-oriented artisan supply chains, enterprise support, training, and quality management linked to orders | Pair market access with production management, skills, and quality systems | A development program and its partners coordinate more directly than a neutral protocol |
| [Otonomi in Lloyd's Lab](https://www.lloyds.com/insights/lloyds-lab/programmes-and-initiatives/lloyds-lab-accelerator/alumni/otonomi) | Blockchain smart-contract parametric cover for air-freight delay and interruption, with underwriting capacity supplied by insurance-market participants | Shipment events can support fast, narrowly defined parametric products while licensed providers carry risk | Cargo-delay cover is not proof of small-garment damage insurance or decentralized underwriting |
| [Insurwave](https://insurwave.ai/insurwave-about.html) | A shared marine-insurance record and live view of asset risk; its original implementation used blockchain before evolving toward SaaS | Shared, permissioned event data can reduce reconciliation and improve risk visibility without making blockchain permanent or mandatory | Designed for complex commercial/marine risks, not individual artisan garments |
| [Etherisc](https://docs.etherisc.com/) | Open-source building blocks for blockchain and parametric insurance products | Open insurance software can inform modular event, oracle, and policy interfaces | Software does not remove licensing, solvency, distribution, claims, or consumer-protection obligations |
| Blockchain-anchored textile passport systems such as [Traced Systems](https://traced.systems/) | Product identifiers and supply-chain records can make provenance data portable and inspectable | Anchor selected claims where useful, while retaining issuer identity and evidence | Vendor claims and anchoring do not guarantee source truth |
| [European Commission Digital Product Passport](https://single-market-economy.ec.europa.eu/single-market/digital-product-passport_en) | A data carrier such as a QR code links a physical product to structured digital information | Use stable identifiers and QR-linked records designed for interoperability | EU DPP policy does not require blockchain; legal applicability and required data vary by product and implementation timetable |

No mature precedent has been identified that combines distributed artisan production, phone-based textile QA, product passports, order-linked finance, fine-grained custody, and insurance at the scale of a single rural artisan garment. The pilot must therefore validate integration assumptions rather than treating adjacent examples as proof.

For context on microcredit, see the primary research synthesis, [*Six Randomized Evaluations of Microcredit: Introduction and Further Steps*](https://economics.mit.edu/sites/default/files/publications/Six%20Randomized%20Evaluations%20of%20Microcredit.pdf), which reports limited average transformative effects alongside meaningful heterogeneity.

## 11. Named entities and reference directory

This directory identifies the named projects, organizations, programs, and examples used in this specification. Inclusion means that a technique or boundary is relevant to study; it is not an endorsement, partnership, or claim that the entity works with lotus fiber or Padama.

| Entity | What it is | Why it is relevant |
| --- | --- | --- |
| **Padama / Padonma** | The open-source protocol and project specified here. Both names have been used for the project; this document uses **Padama** as its specification term. | Supplies interoperable identities, orders, evidence, event records, and reference tools while leaving commerce and regulated services to independent actors. |
| **[BRAC](https://www.brac.net/)** | A Bangladesh-based international development organization and the parent organization behind several social enterprises and programs. It is not the Government of Bangladesh. | Its integrated livelihood, finance, and enterprise experience provides context for producer support, but Padama distributes rather than consolidates these functions. |
| **[Aarong](https://www.brac.net/solutions/social-enterprise/aarong/)** | A BRAC social enterprise and fair-trade fashion/lifestyle brand connecting rural producers with markets. | Demonstrates timely artisan payment, market access, production coordination, and the assumption of inventory and market risk by an intermediary. |
| **Ayesha Abed Foundation (AAF)** | The BRAC-associated foundation at the center of Aarong's network of production centers and sub-centers. | Its hub-and-spoke allocation of orders and materials, preparation, finishing, and QA are useful operational patterns to translate into separable network roles. |
| **Indian Common Facility Centres (CFCs)** | Shared production, processing, testing, training, or business facilities used in Indian cluster-development programs. | Provide a precedent for communal access to intermittently used equipment rather than requiring each artisan to own or finance it individually. |
| **[SFURTI](https://sfurti.msme.gov.in/)** | The Government of India's Scheme of Fund for Regeneration of Traditional Industries, administered through the Ministry of Micro, Small & Medium Enterprises and partner agencies. | Demonstrates cluster organization, shared facilities, skills, and common production capacity; Padama is not a government cluster program. |
| **[India's Ministry of Micro, Small & Medium Enterprises](https://msme.gov.in/)** | The national ministry responsible for SFURTI and other MSME policy and programs. | Provides the primary institutional source for the SFURTI/Common Facility Centre precedent. |
| **Chanderi Handloom Cluster / producer company** | Producer institutions developed among handloom weavers in Chanderi, India, including producer-company approaches to aggregation and market participation. | Offers a case for producer ownership, collective services, and bargaining power. Exact institutional results and current status require field validation before use in a pilot design. |
| **[Trama Textiles](https://tramatextiles.org/)** | A Guatemalan weaving cooperative and artisan-market organization. | Illustrates cooperative producer voice, collective services, and market linkage outside the lotus-fiber sector. |
| **[WomenWeave](https://womenweave.org/)** | An India-based organization supporting handloom livelihoods, skills, design, and market connections. | Shows why training and ecosystem support must be ongoing roles rather than one-time software onboarding. |
| **[UN International Trade Centre (ITC) Ethical Fashion Initiative](https://www.intracen.org/our-work/projects/ethical-fashion-initiative)** | An ITC program connecting artisan enterprises with fashion supply chains and supporting skills, production, and quality management. | Demonstrates market-oriented, order-linked artisan supply-chain development outside lotus fiber. |
| **[Lloyd's](https://www.lloyds.com/)** | A regulated insurance and reinsurance marketplace in which syndicates and other market participants underwrite risks. | Its subscription-market structure is an analogy for multiple underwriters sharing a defined risk; the analogy does not authorize Padama to underwrite. |
| **[Lloyd's Lab](https://www.lloyds.com/insights/lloyds-lab)** | Lloyd's innovation accelerator for insurance concepts and companies. | Provides the institutional context in which Otonomi developed and secured capacity for its cargo-delay product. |
| **[Otonomi](https://www.lloyds.com/insights/lloyds-lab/programmes-and-initiatives/lloyds-lab-accelerator/alumni/otonomi)** | An insurtech offering parametric air-freight delay/interruption cover using blockchain smart contracts, developed through Lloyd's Lab. | Shows that shipment events can drive a narrowly defined parametric cargo product while insurance-market actors provide underwriting capacity. |
| **[Insurwave](https://insurwave.ai/insurwave-about.html)** | A specialty-insurance technology platform originally launched with blockchain and later developed as SaaS, providing shared risk and asset information. | Shows the operational value of a shared marine-insurance record and live risk view, as well as the value of remaining technology-neutral. |
| **[Etherisc](https://docs.etherisc.com/)** | An open-source framework and ecosystem for blockchain-based and parametric insurance products. | Provides reusable technical patterns for policy lifecycles, events, risk pools, and oracles, while also illustrating that code does not replace licensed risk carriers. |
| **[Traced Systems](https://traced.systems/)** | A supply-chain traceability provider associated with blockchain-anchored fashion and textile provenance records. | An adjacent example of product identifiers and provenance events; it does not prove the truth of source data or the complete Padama model. |
| **[European Union Digital Product Passport framework](https://single-market-economy.ec.europa.eu/single-market/digital-product-passport_en)** | An EU product-information framework in which a data carrier, such as a QR code, links a physical item to structured digital information. | Supports the stable-ID and QR-linked passport model. The framework does not inherently require blockchain, and its legal requirements must be evaluated separately. |
| **[European Commission](https://commission.europa.eu/)** | The executive body of the European Union and the publisher of the cited DPP materials. | Provides the primary policy source for the EU DPP framework. |
| **[DHL](https://www.dhl.com/)** | A global logistics and express-carrier group used here only as an illustrative international carrier. | Makes the example custody chain concrete; Padama must remain carrier-neutral and integrate other providers through the same event model. |
| **Myanmar / Burma** | The example origin country in the illustrative custody flow; both common English names are included for clarity. | Grounds the rural-producer-to-international-buyer scenario without asserting that a pilot location or route has been selected. |
| **Paris** | The example destination city in the illustrative custody flow. | Grounds the final international delivery event without implying a committed buyer or pilot destination. |
| **Android** | Google's mobile operating-system ecosystem and the target class of common low-cost phones for the web application. | Establishes an accessibility and device constraint for evidence capture; the protocol itself should remain cross-platform. |
| **[Google](https://www.android.com/)** | The company leading the Android ecosystem. | Named only to identify Android's platform context; it has no proposed Padama governance or service role. |
| **NFT (non-fungible token)** | A transferable blockchain token sometimes used to represent a unique asset or claim. | Explicitly optional; relevant only if transferable on-chain ownership is required. Stable identifiers and signed events are otherwise sufficient. |

## 12. Risks and mitigations

| Risk | Mitigation or test |
| --- | --- |
| A dominant coordinator recreates platform dependency | Portable data, direct contracting, multi-provider directories, exit rights, and monitoring of concentration |
| Buyers impose unattainable or shifting criteria | Versioned criteria fixed at order acceptance; paid change orders; appeal and cancellation rules |
| AI rejects good work or embeds device/material bias | Diverse validation sets, confidence thresholds, human review, subgroup error reporting, and preserved evidence |
| Fabricated photos, weights, identities, or custody scans | Signed capture, cross-party handoffs, anomaly detection, selective audits, and proportionate assurance levels |
| QR code is copied or detached | Bind identifier to product evidence and construction details; record replacement; use tamper-evident attachment where justified |
| Public provenance exposes vulnerable producers | Pseudonymous public views, coarse locations, consent controls, separation of operational/private data, and threat modeling |
| Debt exceeds productive use | Prefer shared assets and patient capital; tie repayable finance to verified orders; affordability checks and hardship procedures |
| Voluntary fund becomes opaque or captured | Independent custody, published rules and accounts, conflict controls, audits, caps, and member oversight |
| Padama is mistaken for a certifier, insurer, or payment service | Clear issuer labels, contractual boundaries, provider-signed statuses, and no custody of premiums, payouts, or purchase funds |
| Blockchain or NFT features add cost without value | Require a written use case, compare signed-database alternatives, and keep core flows chain-independent |
| Poor connectivity or low digital literacy excludes producers | Offline queues, assisted modes, local-language training, simple workflows, and non-smartphone proxy roles with consent |
| Evidence requirements shift unpaid administrative work onto artisans | Measure capture time, price evidence work into orders, minimize fields, and let coordinators provide paid assistance |
| Dispute and reputation systems enable retaliation | Contextual ratings, reason codes, evidence, appeal, anti-retaliation review, and no irreversible universal blacklist |

## 13. Staged pilot

### Stage 0: Field discovery and validation

- Map actual lotus-fiber work, existing intermediaries, wages, throughput, seasonality, and device/connectivity constraints.
- Validate the assumed 20:1 spinner-to-weaver ratio and approximately US$100 loom cost; publish ranges and dates rather than preserving point estimates if evidence varies.
- Identify existing payment, transport, finance, and insurance providers in the pilot jurisdiction.
- Co-design consent, privacy, grievance, and compensation practices with producers.

**Exit criterion:** participants agree on a narrow product, realistic order, evidence burden, and governance safeguards.

### Stage 1: Production records and QR passport

- Run one small paid order using participant profiles, work packages, milestones, external payments, and a stable QR-linked passport.
- Include QR-band specialists and at least one locally built or shared loom where appropriate.
- Record time and cost imposed by every evidence step.

**Exit criterion:** the complete event history can be independently reconstructed, artisans are paid under the agreed terms, and no critical flow depends on a single undocumented operator action.

### Stage 2: Assisted distributed QA

- Add Android evidence capture and one narrow, validated automated measurement or defect flag.
- Keep a human reviewer in the loop and offer an appeal on every rejection.
- Compare automated and human outcomes across devices and conditions.

**Exit criterion:** predefined error, usability, appeal-time, and evidence-cost thresholds are met; otherwise automation remains advisory.

### Stage 3: Shared asset and order-linked finance

- Finance a small number of communal looms using grant/recoverable seed, member contribution, and usage fees.
- Test one buyer advance, supplier-credit, or independent revolving-fund flow using external payment providers.
- Monitor utilization, maintenance, income, repayment burden, exclusions, and multiple borrowing.

**Exit criterion:** the asset has a credible maintenance/replacement path and finance has not shifted disproportionate risk to the poorest participants.

### Stage 4: End-to-end custody and insurance experiment

- Record custody from producer through local courier, hub, international carrier, and buyer.
- Invite licensed providers to quote on the evidence package; if no suitable cover exists, conduct a quote-only or claims-simulation exercise rather than pretending coverage.
- Test damage evidence, missing scan handling, privacy, and dispute paths.

**Exit criterion:** providers find the data useful, participants understand coverage and exclusions, and claim evidence can be assembled without excessive burden.

### Stage 5: Interoperability and provider plurality

- Add a second coordinator, QA provider, and application implementation.
- Export and import the same records using published schemas and conformance tests.
- Evaluate concentration, switching cost, governance representation, security, and financial sustainability.

**Exit criterion:** participants can change providers without losing usable histories or active-order evidence.

## 14. Open questions

1. Which legal entity or community process stewards the protocol schemas, trademarks, reference services, and security response?
2. What minimum identity assurance is needed for each role and transaction value without excluding undocumented or vulnerable producers?
3. Who pays for evidence capture, human QA, appeals, training, data storage, and long-term passport availability?
4. Which product and defect class is narrow enough for the first automated QA validation?
5. What error rates and confidence thresholds are acceptable to producers and buyers, and who bears the cost of false rejection?
6. How are buyer criteria expressed so they are measurable, translatable, and stable through production?
7. What information belongs in public provenance, buyer-only records, provider-only records, and time-limited private evidence?
8. How should a physical QR band be replaced or corrected without breaking product identity?
9. Which event types, if any, justify public-chain anchoring rather than signed records in replicated databases?
10. Is transferable ownership ever required for a garment passport, or would an NFT introduce needless operational and consumer risk?
11. What actual utilization rate, maintenance cost, and governance model make a communal loom sustainable?
12. Which capital providers can offer transparent, order-linked terms in the pilot jurisdiction, and what hardship safeguards are enforceable?
13. Can a licensed insurer economically cover a single garment, or must shipments be pooled by hub, buyer, route, or period?
14. How are loss, damage, delay, workmanship, buyer rejection, and political or customs risks separated so coverage and responsibility remain intelligible?
15. Which dispute resolvers are trusted by rural producers as well as international buyers, and how will language and power imbalances be addressed?
16. What evidence would justify scaling beyond a subsidized pilot, and what evidence would require stopping or redesigning it?
