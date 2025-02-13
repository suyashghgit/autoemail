--
-- PostgreSQL database dump
--

-- Dumped from database version 14.15 (Homebrew)
-- Dumped by pg_dump version 14.15 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: email_metrics; Type: TABLE; Schema: public; Owner: suyashghimire
--

CREATE TABLE public.email_metrics (
    id integer NOT NULL,
    contact_id integer,
    sequence_id integer,
    message_id character varying,
    status character varying,
    sent_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    opened boolean DEFAULT false,
    opened_at timestamp without time zone,
    error_message character varying(255)
);


ALTER TABLE public.email_metrics OWNER TO suyashghimire;

--
-- Name: email_metrics_id_seq; Type: SEQUENCE; Schema: public; Owner: suyashghimire
--

CREATE SEQUENCE public.email_metrics_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.email_metrics_id_seq OWNER TO suyashghimire;

--
-- Name: email_metrics_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: suyashghimire
--

ALTER SEQUENCE public.email_metrics_id_seq OWNED BY public.email_metrics.id;


--
-- Name: mailing_list_user_id_seq; Type: SEQUENCE; Schema: public; Owner: suyashghimire
--

CREATE SEQUENCE public.mailing_list_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mailing_list_user_id_seq OWNER TO suyashghimire;

--
-- Name: mailing_list; Type: TABLE; Schema: public; Owner: suyashghimire
--

CREATE TABLE public.mailing_list (
    user_id integer DEFAULT nextval('public.mailing_list_user_id_seq'::regclass) NOT NULL,
    first_name character varying(100) NOT NULL,
    last_name character varying(100) NOT NULL,
    email_address character varying(255) NOT NULL,
    email_sequence integer DEFAULT 0,
    join_date timestamp with time zone NOT NULL,
    last_email_sent_at timestamp with time zone NOT NULL,
    company_name character varying(255),
    phone_number character varying(20),
    linkedin_url character varying(255),
    notes character varying(255)
);


ALTER TABLE public.mailing_list OWNER TO suyashghimire;

--
-- Name: oauth_credentials; Type: TABLE; Schema: public; Owner: suyashghimire
--

CREATE TABLE public.oauth_credentials (
    id integer NOT NULL,
    credential_type character varying(50) NOT NULL,
    credentials_json text NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.oauth_credentials OWNER TO suyashghimire;

--
-- Name: oauth_credentials_id_seq; Type: SEQUENCE; Schema: public; Owner: suyashghimire
--

CREATE SEQUENCE public.oauth_credentials_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.oauth_credentials_id_seq OWNER TO suyashghimire;

--
-- Name: oauth_credentials_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: suyashghimire
--

ALTER SEQUENCE public.oauth_credentials_id_seq OWNED BY public.oauth_credentials.id;


--
-- Name: sequence_mapping; Type: TABLE; Schema: public; Owner: suyashghimire
--

CREATE TABLE public.sequence_mapping (
    sequence_id integer NOT NULL,
    email_body text,
    article_link character varying(255),
    is_active boolean DEFAULT true,
    email_subject character varying(255)
);


ALTER TABLE public.sequence_mapping OWNER TO suyashghimire;

--
-- Name: sequence_update_history; Type: TABLE; Schema: public; Owner: suyashghimire
--

CREATE TABLE public.sequence_update_history (
    id integer NOT NULL,
    contact_id integer NOT NULL,
    previous_sequence integer NOT NULL,
    new_sequence integer NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.sequence_update_history OWNER TO suyashghimire;

--
-- Name: sequence_update_history_id_seq; Type: SEQUENCE; Schema: public; Owner: suyashghimire
--

CREATE SEQUENCE public.sequence_update_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sequence_update_history_id_seq OWNER TO suyashghimire;

--
-- Name: sequence_update_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: suyashghimire
--

ALTER SEQUENCE public.sequence_update_history_id_seq OWNED BY public.sequence_update_history.id;


--
-- Name: email_metrics id; Type: DEFAULT; Schema: public; Owner: suyashghimire
--

ALTER TABLE ONLY public.email_metrics ALTER COLUMN id SET DEFAULT nextval('public.email_metrics_id_seq'::regclass);


--
-- Name: oauth_credentials id; Type: DEFAULT; Schema: public; Owner: suyashghimire
--

ALTER TABLE ONLY public.oauth_credentials ALTER COLUMN id SET DEFAULT nextval('public.oauth_credentials_id_seq'::regclass);


--
-- Name: sequence_update_history id; Type: DEFAULT; Schema: public; Owner: suyashghimire
--

ALTER TABLE ONLY public.sequence_update_history ALTER COLUMN id SET DEFAULT nextval('public.sequence_update_history_id_seq'::regclass);


--
-- Data for Name: email_metrics; Type: TABLE DATA; Schema: public; Owner: suyashghimire
--

COPY public.email_metrics (id, contact_id, sequence_id, message_id, status, sent_at, opened, opened_at, error_message) FROM stdin;
239	1	1	194fc618d2f76988	delivered	2025-02-12 16:57:19.232708	f	\N	\N
240	2	1	194fc61b5216cdbb	delivered	2025-02-12 16:57:29.638041	f	\N	\N
241	103	1	194fd390edd9cadb	delivered	2025-02-12 20:52:42.663908	f	\N	\N
242	103	15	194fd423857bf92c	delivered	2025-02-12 21:02:43.032167	f	\N	\N
243	103	15	194fd48e37e3638b	delivered	2025-02-12 21:10:00.058831	f	\N	\N
244	2	1	194fd8c0b7f946f0	delivered	2025-02-12 22:23:21.067233	f	\N	\N
245	103	15	194fd8cec81291e8	delivered	2025-02-12 22:24:18.808789	f	\N	\N
246	103	15	194fd94e86f3c8dd	delivered	2025-02-12 22:33:02.444968	f	\N	\N
247	103	15	194fdb0c68909767	delivered	2025-02-12 23:03:28.412792	f	\N	\N
\.


--
-- Data for Name: mailing_list; Type: TABLE DATA; Schema: public; Owner: suyashghimire
--

COPY public.mailing_list (user_id, first_name, last_name, email_address, email_sequence, join_date, last_email_sent_at, company_name, phone_number, linkedin_url, notes) FROM stdin;
1	Suyash	Ghimire	a@mail.com	6	2025-01-08 16:57:17.359879-06	2025-02-12 16:57:17.359883-06		2144634297		\N
102	Suyash	Ghimire	c@gmail.com	7	2025-01-01 16:57:17.359879-06	2025-02-12 16:57:17.359883-06	\N	\N	\N	\N
2	Suyash	Ghimire	b@mail.com	1	2025-02-12 16:57:28.089358-06	2025-02-12 22:23:21.067435-06		2144634297		\N
103	Suyash	Ghimire	suyashghimire3000@gmail.com	15	2025-02-12 20:52:40.860129-06	2025-02-12 23:03:28.412868-06		2144634297		\N
\.


--
-- Data for Name: oauth_credentials; Type: TABLE DATA; Schema: public; Owner: suyashghimire
--

COPY public.oauth_credentials (id, credential_type, credentials_json, created_at, updated_at) FROM stdin;
1	client_secret	{\n        "web": {\n            "client_id": "105157187942-89ha5k01sv2ajtqqc834or657821ajm3.apps.googleusercontent.com",\n            "project_id": "skilful-bearing-450622-r1",\n            "auth_uri": "https://accounts.google.com/o/oauth2/auth",\n            "token_uri": "https://oauth2.googleapis.com/token",\n            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",\n            "client_secret": "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",\n            "redirect_uris": [\n                "http://localhost:8000/oauth2callback",\n                "http://127.0.0.1:8000/oauth2callback",\n                "http://localhost:8000/auth/callback"\n            ],\n            "javascript_origins": [\n                "http://localhost:8000",\n                "http://127.0.0.1:8000"\n            ]\n        }\n    }	2025-02-12 22:11:24.153216-06	2025-02-12 22:11:24.153216-06
4	token	{"token": "ya29.a0AXeO80RPiA7_nCuDOSveEf0xIysXTFLGufc8ZWqaEcTj188QTNGiGT2eisn2by8ZPT5MVKXOcnecHfSm4IIA80NweRPXy6IaYl7fd6XXK0cx7ss8_O3m57AmD7EEdlmbnACjfQVmeECZYLIUdm5bng_YoeqHV0i4qbz1_OUe_QaCgYKAdYSARMSFQHGX2MipUUQZwnwZgTpOJJcyEXalw0177", "refresh_token": null, "token_uri": "https://oauth2.googleapis.com/token", "client_id": "105157187942-89ha5k01sv2ajtqqc834or657821ajm3.apps.googleusercontent.com", "client_secret": "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", "scopes": ["https://www.googleapis.com/auth/gmail.send"], "expiry": "2025-02-13T06:03:18.639564"}	2025-02-12 23:03:19.644551-06	2025-02-12 23:03:19.644556-06
\.


--
-- Data for Name: sequence_mapping; Type: TABLE DATA; Schema: public; Owner: suyashghimire
--

COPY public.sequence_mapping (sequence_id, email_body, article_link, is_active, email_subject) FROM stdin;
6	<p>I wanted to personally bring to your attention an article I recently wrote regarding the SEC's extension of the compliance date for short sale reporting and its implications for issuers and shareholders. This delay creates an opportunity for immediate action, and the US~Observer is prepared to expose manipulative trading practices that continue to harm businesses and investors.</p><ul><li>Through investigative journalism, we can uncover and correct these wrongdoings, ensuring transparency and accountability in financial markets. I believe this is a critical issue that warrants your attention, and I would appreciate the opportunity to discuss how we can address it in your company effectively.</li></ul><p><br></p>	https://usobserver.com/who-is-guarding-the-hen-house/	f	Who is guarding the hen house
15	<p>I wanted to personally bring to your attention an article I recently wrote regarding the SEC's extension of the compliance date for short sale reporting and its implications for issuers and shareholders. This delay creates an opportunity for immediate action, and the US~Observer is prepared to expose manipulative trading practices that continue to harm businesses and investors.</p><p>Through investigative journalism, we can uncover and correct these wrongdoings, ensuring transparency and accountability in financial markets. I believe this is a critical issue that warrants your attention, and I would appreciate the opportunity to discuss how we can address it in your company effectively.</p>	https://ekantipur.com/news/2025/02/13/due-to-the-negligence-of-the-electricity-authority-3-million-liters-of-water-was-wasted-when-the-pipe-of-melamchi-burst-16-34.html	f	SEC's extension of the compliance date for short sale
1	<p>I wanted to personally bring to your attention an article I recently wrote regarding the SEC's extension of the compliance date for short sale reporting and its implications for issuers and shareholders. This delay creates an opportunity for immediate action, and the US~Observer is prepared to expose manipulative trading practices that continue to harm businesses and investors.</p><ul><li>Through investigative journalism, we can uncover and correct these wrongdoings, ensuring transparency and accountability in financial markets. I believe this is a critical issue that warrants your attention, and I would appreciate the opportunity to discuss how we can address it in your company effectively.</li></ul>	https://usobserver.com/who-is-guarding-the-hen-house/	f	Who is guarding the hen house
4	<p>I wanted to personally bring to your attention an article I recently wrote regarding the SEC's extension of the compliance date for short sale reporting and its implications for issuers and shareholders. This delay creates an opportunity for immediate action, and the US~Observer is prepared to expose manipulative trading practices that continue to harm businesses and investors.</p><ul><li>Through investigative journalism, we can uncover and correct these wrongdoings, ensuring transparency and accountability in financial markets. I believe this is a critical issue that warrants your attention, and I would appreciate the opportunity to discuss how we can address it in your company effectively.</li></ul><p><br></p>	https://usobserver.com/countering-the-abusive-short-sell-is-now-an-option/	f	Countering the abusive short sell
3	<p>I wanted to personally bring to your attention an article I recently wrote regarding the SEC's extension of the compliance date for short sale reporting and its implications for issuers and shareholders. This delay creates an opportunity for immediate action, and the US~Observer is prepared to expose manipulative trading practices that continue to harm businesses and investors.</p><ul><li>Through investigative journalism, we can uncover and correct these wrongdoings, ensuring transparency and accountability in financial markets. I believe this is a critical issue that warrants your attention, and I would appreciate the opportunity to discuss how we can address it in your company effectively.</li></ul><p><br></p>	https://usobserver.com/fraud-schemes-and-cons-begone/	t	Fraud schemes and cons
5	<p>I wanted to personally bring to your attention an article I recently wrote regarding the SEC's extension of the compliance date for short sale reporting and its implications for issuers and shareholders. This delay creates an opportunity for immediate action, and the US~Observer is prepared to expose manipulative trading practices that continue to harm businesses and investors.</p><ul><li>Through investigative journalism, we can uncover and correct these wrongdoings, ensuring transparency and accountability in financial markets. I believe this is a critical issue that warrants your attention, and I would appreciate the opportunity to discuss how we can address it in your company effectively.</li></ul><p><br></p>	https://usobserver.com/reputation-is-everything/	f	Reputation is everything
8	\N	\N	f	\N
7	\N	\N	f	\N
9	<p>Hi,</p><p>This is week 1.</p><ul><li><strong>Investigation &amp; Exposure - </strong>We uncover the truth and&nbsp;<strong>threaten to expose</strong>&nbsp;wrongdoers. If necessary, we follow through—publicly&nbsp;</li></ul>	https://usobserver.com/exposing-naked-shorts-obtaining-justice-and-shareholder-protection/	f	\N
10	\N	\N	f	\N
2	<p>I wanted to personally bring to your attention an article I recently wrote regarding the SEC's extension of the compliance date for short sale reporting and its implications for issuers and shareholders. This delay creates an opportunity for immediate action, and the US~Observer is prepared to expose manipulative trading practices that continue to harm businesses and investors.</p><ul><li>Through investigative journalism, we can uncover and correct these wrongdoings, ensuring transparency and accountability in financial markets. I believe this is a critical issue that warrants your attention, and I would appreciate the opportunity to discuss how we can address it in your company effectively.</li></ul>	https://hello.com/	t	SEC Investigation five years
\.


--
-- Data for Name: sequence_update_history; Type: TABLE DATA; Schema: public; Owner: suyashghimire
--

COPY public.sequence_update_history (id, contact_id, previous_sequence, new_sequence, updated_at) FROM stdin;
\.


--
-- Name: email_metrics_id_seq; Type: SEQUENCE SET; Schema: public; Owner: suyashghimire
--

SELECT pg_catalog.setval('public.email_metrics_id_seq', 247, true);


--
-- Name: mailing_list_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: suyashghimire
--

SELECT pg_catalog.setval('public.mailing_list_user_id_seq', 102, true);


--
-- Name: oauth_credentials_id_seq; Type: SEQUENCE SET; Schema: public; Owner: suyashghimire
--

SELECT pg_catalog.setval('public.oauth_credentials_id_seq', 4, true);


--
-- Name: sequence_update_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: suyashghimire
--

SELECT pg_catalog.setval('public.sequence_update_history_id_seq', 1, false);


--
-- Name: email_metrics email_metrics_pkey; Type: CONSTRAINT; Schema: public; Owner: suyashghimire
--

ALTER TABLE ONLY public.email_metrics
    ADD CONSTRAINT email_metrics_pkey PRIMARY KEY (id);


--
-- Name: mailing_list mailing_list_email_address_key; Type: CONSTRAINT; Schema: public; Owner: suyashghimire
--

ALTER TABLE ONLY public.mailing_list
    ADD CONSTRAINT mailing_list_email_address_key UNIQUE (email_address);


--
-- Name: mailing_list mailing_list_pkey; Type: CONSTRAINT; Schema: public; Owner: suyashghimire
--

ALTER TABLE ONLY public.mailing_list
    ADD CONSTRAINT mailing_list_pkey PRIMARY KEY (user_id);


--
-- Name: oauth_credentials oauth_credentials_pkey; Type: CONSTRAINT; Schema: public; Owner: suyashghimire
--

ALTER TABLE ONLY public.oauth_credentials
    ADD CONSTRAINT oauth_credentials_pkey PRIMARY KEY (id);


--
-- Name: sequence_mapping sequence_mapping_pkey; Type: CONSTRAINT; Schema: public; Owner: suyashghimire
--

ALTER TABLE ONLY public.sequence_mapping
    ADD CONSTRAINT sequence_mapping_pkey PRIMARY KEY (sequence_id);


--
-- Name: sequence_update_history sequence_update_history_pkey; Type: CONSTRAINT; Schema: public; Owner: suyashghimire
--

ALTER TABLE ONLY public.sequence_update_history
    ADD CONSTRAINT sequence_update_history_pkey PRIMARY KEY (id);


--
-- Name: idx_email_metrics_contact_id; Type: INDEX; Schema: public; Owner: suyashghimire
--

CREATE INDEX idx_email_metrics_contact_id ON public.email_metrics USING btree (contact_id);


--
-- Name: idx_email_metrics_sent_at; Type: INDEX; Schema: public; Owner: suyashghimire
--

CREATE INDEX idx_email_metrics_sent_at ON public.email_metrics USING btree (sent_at);


--
-- Name: idx_sequence_update_history_contact_id; Type: INDEX; Schema: public; Owner: suyashghimire
--

CREATE INDEX idx_sequence_update_history_contact_id ON public.sequence_update_history USING btree (contact_id);


--
-- Name: idx_sequence_update_history_updated_at; Type: INDEX; Schema: public; Owner: suyashghimire
--

CREATE INDEX idx_sequence_update_history_updated_at ON public.sequence_update_history USING btree (updated_at DESC);


--
-- Name: email_metrics email_metrics_contact_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: suyashghimire
--

ALTER TABLE ONLY public.email_metrics
    ADD CONSTRAINT email_metrics_contact_id_fkey FOREIGN KEY (contact_id) REFERENCES public.mailing_list(user_id);


--
-- Name: sequence_update_history sequence_update_history_contact_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: suyashghimire
--

ALTER TABLE ONLY public.sequence_update_history
    ADD CONSTRAINT sequence_update_history_contact_id_fkey FOREIGN KEY (contact_id) REFERENCES public.mailing_list(user_id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

