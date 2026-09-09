# Knowledge Base Index

| Article | Summary | Compiled From | Updated |
|---------|---------|---------------|---------|
| [[concepts/claude-code-hooks-windows-execution]] | Claude Code runs hooks via Git Bash on Windows; backslash paths silently fail | daily/2026-05-06.md | 2026-05-06 |
| [[concepts/sessionend-hook-debugging]] | Sentinel-file approach to diagnose whether SessionEnd hooks are firing at all | daily/2026-05-06.md | 2026-05-06 |
| [[concepts/windows-path-forward-slash-git-bash]] | Forward slashes are the safe cross-context path format on Windows for Git Bash and Python | daily/2026-05-06.md | 2026-05-06 |
| [[concepts/keycrm-mcp-get-lead-notes-fix]] | get_lead_notes was broken; fix uses GET /communications/comments/lead/{id}; MCP reload via taskkill /F /IM node.exe | daily/2026-05-06.md | 2026-06-12 |
| [[concepts/keycrm-pipeline-specific-statuses]] | Status codes are pipeline-bound; wrong status silently transfers a lead to another pipeline | daily/2026-05-06.md | 2026-05-19 |
| [[concepts/keycrm-raw-record-processing-algorithm]] | Structured algorithm: comment → daily note → one-frame confirmation block → follow-up with deadlines | daily/2026-05-06.md | 2026-05-15 |
| [[concepts/viber-message-proactive-closing]] | Most Viber messages end with a proactive call announcement; exception: after contract + invoice, end with a direct CTA | daily/2026-05-06.md | 2026-05-19 |
| [[concepts/keycrm-post-delivery-payment-clients]] | Clients refusing prepayment require a separate track: park at status 148, return when stock available | daily/2026-05-06.md | 2026-05-06 |
| [[concepts/rgs-advance-document-preparation]] | RGS passport and calibration table can be prepared before tank completion to accelerate client licensing | daily/2026-05-06.md | 2026-05-06 |
| [[concepts/tender-gated-lead-management]] | B2B leads in active internal tenders must be parked until tender result + signed contract received | daily/2026-05-13.md | 2026-05-19 |
| [[concepts/multi-variant-kp-price-anchoring]] | Present 2–3 equipment variants without total sum; optional items go in separate add-ons block; deadline discount applies to all variants | daily/2026-05-13.md | 2026-06-16 |
| [[concepts/vialon-fuel-identification-upsell]] | Vialon fuel ID system (36k ПДВ) adds card-blocking, mobile control, and monthly reports; in multi-variant КPs goes in "Додатково" block | daily/2026-05-13.md | 2026-06-16 |
| [[concepts/keycrm-competitor-loss-closure]] | Close as status 9 when client confirms competitor purchase; record contact for future re-engagement | daily/2026-05-14.md | 2026-05-19 |
| [[concepts/keycrm-pre-kp-spec-clarification]] | Delegate spec/price check internally before sending KP when client requirement is non-standard | daily/2026-05-14.md | 2026-05-19 |
| [[concepts/keycrm-overdue-nc-recovery]] | Re-read brief and update NC to nearest date when next-contact date has passed without a call | daily/2026-05-14.md | 2026-05-19 |
| [[concepts/kb-index-consistency-checking]] | Index summaries can diverge from article bodies; fix the summary not the article; CLAUDE.md is a derived source | daily/2026-05-19.md | 2026-05-20 |
| [[concepts/keycrm-rgs-cleaning-acts-commissioning]] | Cleaning acts (акти зачистки) required per branch; акти виконання робіт follow as second phase; assign to Матлаш/Біндус | daily/2026-05-20.md | 2026-05-26 |
| [[concepts/keycrm-advance-payment-control]] | After contract + invoice: status → Аванс, NC next day, critical payment control task, Viber with signing instructions | daily/2026-05-20.md | 2026-05-20 |
| [[concepts/keycrm-budget-process-gating]] | Budget session (сесія → виділення коштів) gates the deal; park with NC at expected session date, prepare ВП-запит in advance | daily/2026-05-21.md | 2026-05-21 |
| [[concepts/rgs-fuel-storage-capacity-norms]] | Regulatory 45t fuel reserve norm drives sizing: 30m³ AZS insufficient, single РГС-50 marginal, 2×РГС-50 compliant | daily/2026-05-21.md | 2026-05-21 |
| [[concepts/keycrm-daily-funnel-brief]] | 4-block brief: Гроші в роботі (excl. Нараховано), ТОП ВОРОНКИ (A+B at-risk), Дзвонити сьогодні, Критичні; limit 10/block | daily/2026-05-21.md | 2026-05-29 |
| [[concepts/keycrm-abc-score-update-sequence]] | Update status before calling update_card_fields; ABC calculated against old status if sequence is reversed; race condition can score 0 pipeline points even with correct ordering | daily/2026-05-25.md | 2026-07-20 |
| [[concepts/keycrm-intermediary-contact-handling]] | Leads from an intermediary (посередник) go to status 59 (Уточнення контакту), not 2 (Ідентифікація) | daily/2026-05-25.md | 2026-05-26 |
| [[concepts/keycrm-seasonal-lead-parking]] | Agricultural season gates deals → КП пауза (72/148); long-term deferral with intact intent → КП пауза, not Зміна планів | daily/2026-05-25.md | 2026-06-11 |
| [[concepts/keycrm-client-requisites-invoice-trigger]] | Client proactively sending bank requisites signals payment readiness; jump directly to Рахунок (38), skip intermediate stages | daily/2026-05-25.md | 2026-05-26 |
| [[concepts/keycrm-tz-document-control]] | When client commits to sending a ТЗ, create a document control task with NC on expected delivery date | daily/2026-05-25.md | 2026-05-26 |
| [[concepts/keycrm-mcp-get-card-raw-duplicate-response]] | get_card_raw returns card + internalCard as a full duplicate; at 65 calls/day this drives ~130K tokens in briefing | daily/2026-05-26.md | 2026-05-26 |
| [[concepts/keycrm-briefing-token-optimization]] | Slim Briefing Script (direct API + 5 fields) cuts briefing from 130K → ~750 tokens; start with SessionStart trim, then briefing_fetch.py | daily/2026-05-26.md | 2026-05-26 |
| [[concepts/keycrm-client-address-convention]] | Address clients with vocative case + "доброго дня" in all Viber messages and calls | daily/2026-05-26.md | 2026-05-26 |
| [[concepts/keycrm-partial-scope-lead-recovery]] | When one product in a multi-item lead is sourced elsewhere, re-scope and re-enter КП підготовка for remaining items | daily/2026-05-26.md | 2026-05-29 |
| [[concepts/keycrm-silent-lead-vp-template]] | Viber reactivation template for unreachable clients: "Намагались додзвонитись / [reference] / Актуально ще чи вже вирішили питання?" | daily/2026-05-28.md | 2026-05-29 |
| [[concepts/keycrm-non-responsive-lead-criteria]] | Status 88 threshold: 12+ days silence + call unanswered → send reactivation ВП first, then close as non-responsive if no reply | daily/2026-05-28.md | 2026-05-29 |
| [[concepts/keycrm-pipeline-stage-semantics]] | Рахунок=договір+реквізити, Аванс=рахунок виставлено, Виробництво=аванс зайшов; Маркетинг ВАЙБЕР/СМС — відмова з потенціалом (вайбер/без) | session/2026-06-02 | 2026-06-02 |
| [[concepts/keycrm-deal-checklist]] | Живий чеклист угоди в полі "Замітка" картки (manager_comment); формат позначок ✅/⬜/⏳ по кожному переходу статусу; manager_comment ще не підтримується update_lead | session/2026-06-02 | 2026-06-02 |
| [[concepts/powershell-utf8-file-handling]] | Get-Content без кодування ламає кирилицю; використовувати [System.IO.File]::ReadAllText/WriteAllText з UTF8 | session/2026-06-02 | 2026-06-02 |
| [[concepts/keycrm-zamitka-mcp-limitation]] | add_note writes to comments, not the Замітка field; update_lead lacks a Замітка param — checklist workaround via comments until MCP is patched | daily/2026-06-02.md | 2026-06-02 |
| [[concepts/keycrm-competitor-kp-counter-respec]] | Client submitting competitor's KP is a buying signal; respec to client's own ТЗ, not the competitor's configuration | daily/2026-06-02.md | 2026-06-02 |
| [[concepts/keycrm-skill-file-status-bugs]] | Wrong status IDs and wrong API call ordering in skill files cause silent CRM errors; audit scope expanded in July 2026 | daily/2026-06-10.md, daily/2026-07-17.md | 2026-07-17 |
| [[concepts/keycrm-rgs-prk-vp-template]] | РГС+ПРК Viber proposal template: котушка, сума без знижки, гарантія 18 міс, документи ліцензії as separate closing block | daily/2026-06-11.md | 2026-06-11 |
| [[concepts/keycrm-update-card-fields-404-error]] | update_card_fields returns 404 on some leads, silently failing to write ОБЛАСТЬ/Обʼєм/АВС custom fields | daily/2026-06-11.md | 2026-06-11 |
| [[concepts/keycrm-kdz-vs-kp-pauza-licensing-pause]] | Client-initiated pause → КДЗ (189); manager-scheduled wait → КП пауза (72); diagnostic test: "рішення зріє зараз?" | daily/2026-06-11.md | 2026-07-20 |
| [[concepts/keycrm-mcp-update-lead-title]] | update_lead lacks title by default; add title param to index.js + taskkill node.exe to reload MCP | daily/2026-06-12.md | 2026-06-12 |
| [[concepts/keycrm-lead-naming-convention]] | Template: ПІДПРИЄМСТВО CAPS * Локація * Продукт * Ім'я * +телефон; periodic audit renames auto-created cards | daily/2026-06-12.md | 2026-06-12 |
| [[concepts/keycrm-facebook-lead-data-gaps]] | Facebook leads often arrive without phone in CRM card; check notes/comments before renaming or processing | daily/2026-06-12.md | 2026-06-12 |
| [[concepts/keycrm-kp-optional-addons-block]] | Optional items (Vialon, котушка) go in "Додатково можемо запропонувати" block — never folded into the main KP total | daily/2026-06-16.md | 2026-06-16 |
| [[concepts/keycrm-deadline-discount-anchor]] | Apply 3–5% discount until a near-term date on all KP variants as an urgency anchor; deadline becomes the follow-up call hook | daily/2026-06-16.md | 2026-06-16 |
| [[concepts/keycrm-abc-amount-field-mismatch]] | `update_card_fields` read `products_total` instead of `amount`, causing ABC deal-size to always score 0; fixed June 2026 | daily/2026-06-25.md | 2026-06-25 |
| [[concepts/claude-md-maintenance-workflow]] | Periodic audit of session logs to identify gaps in CLAUDE.md; batch-confirm changes; backup before applying | daily/2026-06-25.md | 2026-06-25 |
| [[concepts/keycrm-vp-chain-multi-variant]] | Send sequential VP messages for multi-fuel-type leads: per-fuel ТТХ → works list → add-ons → confirmation VP after KP | daily/2026-07-02.md | 2026-07-02 |
| [[concepts/keycrm-card-location-mismatch]] | Card title city vs comment city mismatch: flag, defer ОБЛАСТЬ update, verify on next call | daily/2026-07-02.md | 2026-07-02 |
| [[concepts/keycrm-vp-post-kp-decision-framing]] | Post-КП VP closing must name client's decision + next action, not describe the call process | daily/2026-07-07.md | 2026-07-08 |
| [[concepts/keycrm-internal-task-daily-note-tracking]] | Task tool is ephemeral (session-only); persistent internal coordination goes in daily note "🔧 Внутрішні" with DD.MM prefix + ⚠️ aging | daily/2026-07-07.md | 2026-07-08 |
| [[concepts/claude-code-cursor-bug-windows-terminal]] | Claude Code TUI forces block cursor on Windows Terminal; fix: two keys in cachedGrowthBookFeatures (`tengu_native_cursor: true` + `showSpinnerTree: false`) | daily/2026-07-08.md | 2026-07-08 |
| [[concepts/anthropic-oauth-vs-api-key]] | `sk-ant-oat01` = OAuth subscription token (не API-ключ); `sk-ant-api03` = platform API key з console.anthropic.com — лише він підходить для сторонніх застосунків | daily/2026-07-17.md | 2026-07-17 |
| [[concepts/vault-secrets-in-git-repos]] | Два паттерни витоку секретів: Bearer-токен у tracked Python-файлі; GitHub PAT у URL remote у `.git/config`; митигація — .env + .gitignore + SSH | daily/2026-07-17.md | 2026-07-17 |
| [[concepts/anthropic-api-credit-mcp-cascade]] | HTTP 400 "credit balance too low" = вичерпані API-кредити; cascade-ефект вимикає MCP-сервер; taskkill не допомагає — потрібен повний перезапуск після поповнення | daily/2026-07-17.md | 2026-07-17 |
| [[concepts/flush-py-exit-code-1-failure]] | flush.py crashes with exit code 1 causing full-day session capture blackout; root cause: DETACHED_PROCESS flag contradicts inline comment; run directly to surface real exception | daily/2026-07-22.md | 2026-09-04 |
