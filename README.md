# 🏢 Django Real Estate & Agent CRM Platform

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.x-darkgreen.svg?logo=django&logoColor=white)](https://djangoproject.com)
[![Status](https://img.shields.io/badge/Status-Core%20MVP%20%2F%20Customizable-orange.svg)](#)
[![Language](https://img.shields.io/badge/Language-Persian%20(RTL)%20%7C%20EN%20Roadmap-blueviolet.svg)](#)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> A production-ready, scalable foundation bridging modern real estate marketplace listings with an internal CRM workflow for agency teams.

---

> 🌐 **Language & Localization Note:**  
> The current release features a fully functional **Persian (Farsi / RTL)** user interface tailored for regional agency operations. The codebase is architected with Django's native internationalization (`i18n`) standards, and full **English (LTR)** localization is in active development for the next update.

---

## 🌟 Overview & Architecture Philosophy

Most open-source real estate projects are either simple listing blogs or rigid, outdated scripts. This platform is purposefully engineered as an **Open-Core & White-Label Architecture**:

- **Stable Core (Open Source):** Contains the essential database schema, role-based workflows (RBAC), cascading location filters, and listing lifecycle management.
- **Enterprise-Ready Extensibility:** Modularly structured so that real estate agencies, brokerages, and businesses can rapidly deploy, customize, or connect bespoke integrations (SMS/OTP, custom commissions, banking gateways, or headless frontends).

---

## 🚀 Core Features (Available in this Repo)

### 👔 Agent & Consultant CRM
- **Role-Based Access Control (RBAC):** Clean custom mixins protecting agent-only views, preventing unauthorized access with graceful redirects and contextual feedback.
- **Lead & Contact Management:** Dedicated tracking pipelines for buyer/renter inquiries versus seller/landlord properties.
- **Task & Daily Activity Logs:** Daily to-do items and call tracking for proactive agent follow-ups.
- **Soft Archiving:** Archive inactive leads and past listings without losing historical business metrics.

### 🏡 Smart Listings & Public Marketplace
- **Two-Way Marketplace Model:** Distinct modules for *Property Offers* (Sale/Rent) and *Property Requests* (Inquiries/Requirements).
- **Cascading Dynamic Filtering:** AJAX-driven Province ➔ City ➔ Neighborhood selection without full-page reloads.
- **Session-Based City Awareness:** Remembers selected regional preferences across the user browsing session (similar to leading classified platforms).
- **Multi-Step Submission Wizard:** High-conversion listing submission flow splitting complex property metadata into logical steps.

### 🔐 Architecture & Clean Code
- **Custom User Model & Profiles:** Decoupled profile architecture with granular role management.
- **Optimized Queries:** Leveraged `select_related` and `prefetch_related` across nested relations to prevent N+1 query overhead.
- **i18n Scaffolding:** Prepared using Django's gettext and localization conventions for seamless language switching.

---

## 🗺️ Roadmap & Upcoming Releases

- [x] Core MVP release with Persian (RTL) interface
- [x] Location cascading AJAX module
- [ ] English (EN / LTR) language pack & locale switcher
- [ ] RESTful API endpoints via Django REST Framework (DRF)
- [ ] Docker containerization (`docker-compose.yml`)

---

## 💼 Core Open Version vs. Enterprise / Custom Extensions

This repository provides the rock-solid base engine. For businesses and agencies requiring tailor-made extensions, the architecture is ready to integrate:

| Feature Dimension | Core Engine (Open Source) | Enterprise / Custom Extensions |
| :--- | :--- | :--- |
| **Authentication** | Session / Cookie + Custom RBAC | SMS / OTP Gateways (Kavenegar, Twilio) + Social Auth |
| **Localization** | Persian (RTL) | Multi-language switcher (Persian & English) |
| **Monetization** | Free listing submissions | Paid listing tiers, featured ads, and Payment Gateways |
| **Communication** | Internal note logs & call trackers | Real-time chat (Django Channels) & automated SMS alerts |
| **Frontend Options** | Django MVT + Bootstrap & AJAX | Decoupled Headless APIs (DRF) + Angular / React Web Apps |
| **Reporting & BI** | Core database metrics & CSV exports | Visual KPI dashboards, commission splits & team leaderboards |

---

## 🛠️ Tech Stack

- **Backend:** Python 3.11+, Django 5.x (Class-Based Views, Custom Mixins, Signals)
- **Database:** PostgreSQL (Production recommended) / SQLite (Dev)
- **Frontend:** HTML5, CSS3, SCSS, Bootstrap 5 (RTL), JavaScript (Fetch API & jQuery for cascading DOM logic)
- **Security:** CSRF Protection, Custom Access Guards, Secure Sessions

---

## ⚡ Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/amirrezaseydi1/django-RealEstate-CRM.git

cd django-RealEstate-CRM
