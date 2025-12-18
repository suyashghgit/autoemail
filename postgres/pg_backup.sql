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

-- Drop sequences first
DROP SEQUENCE IF EXISTS public.email_metrics_id_seq CASCADE;
DROP SEQUENCE IF EXISTS public.mailing_list_user_id_seq CASCADE;
DROP SEQUENCE IF EXISTS public.mailing_list_user_id_seq1 CASCADE;
DROP SEQUENCE IF EXISTS public.oauth_credentials_id_seq CASCADE;
DROP SEQUENCE IF EXISTS public.sequence_update_history_id_seq CASCADE;

-- Drop existing tables
DROP TABLE IF EXISTS public.email_metrics CASCADE;
DROP TABLE IF EXISTS public.mailing_list CASCADE;
DROP TABLE IF EXISTS public.oauth_credentials CASCADE;
DROP TABLE IF EXISTS public.sequence_mapping CASCADE;
DROP TABLE IF EXISTS public.sequence_update_history CASCADE;

-- Now create tables
CREATE TABLE public.email_metrics (
    id integer NOT NULL,
    contact_id integer,
    sequence_id integer,
    message_id character varying(255),
    history_id character varying(255),
    status character varying(50),
    sent_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    opened_at timestamp without time zone,
    opened boolean DEFAULT false
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
-- Name: mailing_list; Type: TABLE; Schema: public; Owner: suyashghimire
--

CREATE TABLE public.mailing_list (
    user_id integer NOT NULL,
    first_name character varying(100) NOT NULL,
    last_name character varying(100) NOT NULL,
    email_address character varying(255) NOT NULL,
    company_name character varying(255),
    phone_number character varying(50),
    linkedin_url character varying(255),
    email_sequence integer DEFAULT 0,
    join_date timestamp with time zone NOT NULL,
    last_email_sent_at timestamp with time zone NOT NULL,
    notes text
);


ALTER TABLE public.mailing_list OWNER TO suyashghimire;

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
-- Name: mailing_list_user_id_seq1; Type: SEQUENCE; Schema: public; Owner: suyashghimire
--

CREATE SEQUENCE public.mailing_list_user_id_seq1
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mailing_list_user_id_seq1 OWNER TO suyashghimire;

--
-- Name: mailing_list_user_id_seq1; Type: SEQUENCE OWNED BY; Schema: public; Owner: suyashghimire
--

ALTER SEQUENCE public.mailing_list_user_id_seq1 OWNED BY public.mailing_list.user_id;


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
-- Name: mailing_list user_id; Type: DEFAULT; Schema: public; Owner: suyashghimire
--

ALTER TABLE ONLY public.mailing_list ALTER COLUMN user_id SET DEFAULT nextval('public.mailing_list_user_id_seq1'::regclass);


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



--
-- Data for Name: mailing_list; Type: TABLE DATA; Schema: public; Owner: suyashghimire
--

COPY public.mailing_list (user_id, first_name, last_name, email_address, company_name, phone_number, linkedin_url, email_sequence, join_date, last_email_sent_at, notes) FROM stdin;
1	Greg	Chodaczek	ir@telabio.com	TELA Bio, Inc.	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	TELA
2	Ramy	Mahmoud	ramy.mahmoud@optinose.com	OptiNose, Inc.	(267) 364-3500	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	OPTN
3	Peter	Miller	peter.miller@optinose.com	OptiNose, Inc.	(267) 364-3500	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	OPTN
4	Jonathan	Neely	jonathan.neely@optinose.com	OptiNose, Inc.	(978) 868-5011	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	OPTN
5	Vince	Caruso	vince.caruso@newtothestreet.com	Byrna Technologies Inc.	(631) 465-0284	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	BYRN
6	Stanley	Baumgartner	info@securitydii.com	Byrna Technologies Inc.	(905) 582-6402	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	BYRN
7	Lisa	Wager	lisa@byrna.com	Byrna Technologies Inc.	(978) 686-5011	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	BYRN
8	Doug	Lipton	douglipton@msn.com	Byrna Technologies Inc.	(978) 686-5011	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	BYRN
9	Bryan	Ganz	bryan@byrna.com	Byrna Technologies Inc.	(978) 868-5011	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	BYRN
10	Alex	Persson	alex@wecommerce.co	WeCommerce Holdings Ltd.	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	WE.V
11	Jacob	Chacko	jacob.chacko@oricpharma.com	ORIC Pharmaceuticals, Inc.	(650) 388-5600	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	ORIC
12	Dominic	Piscitelli	dominic.piscitelli@oricpharma.com	ORIC Pharmaceuticals, Inc.	(650) 388-5600	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	ORIC
13	Anthony	Cutrone	acutrone@medallion.com	Medallion Financial Corp.	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	MFIN
14	Andrew	Murstein	amurstein@medallion.com	Medallion Financial Corp.	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	MFIN
15	Tomer	Cohen	tcohen@clarkeinc.com	INmune Bio, Inc.	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	INMB
16	David	Moss	dmoss@inmunebio.com	INmune Bio, Inc.	(858) 456-8457	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	INMB
17	Cory	Ellspermann	cellspermann@inmunebio.com	INmune Bio, Inc.	(858) 964-3720	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	INMB
18	Kewa	Luo	ir@kandigroup.com	Kandi Technologies Group, Inc.	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	KNDI
19	Matt	Clawson	ir@singulargenomics.com	Singular Genomics Systems, Inc.	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	OMIC
20	Dan	Budwick	dan@1abmedia.com	Singular Genomics Systems, Inc.	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	OMIC
21	Vikram	Jog	vikram.jog@fluidigm.com	Standard BioTools Inc.	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	LAB
22	Theresa	Royer	theresa.royer@standardbio.com	Standard BioTools Inc.	(855) 859-2056	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	LAB
23	Michael	Egholm	michael.egholm@standardbio.com	Standard BioTools Inc.	(855) 859-2056	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	LAB
24	Mark	Spearman	mark.spearman@fluidigm.com	Standard BioTools Inc.	(855) 859-2056	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	LAB
25	Jeremy	Davis	jeremy.davis@fluidigm.com	Standard BioTools Inc.	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	LAB
26	Anders	Davas	anders.davas@fluidigm.com	Standard BioTools Inc.	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	LAB
27	Alex	Kim	alex.kim@fluidigm.com	Standard BioTools Inc.	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	LAB
28	James	Lawson	jim@adtheorent.com	AdTheorent Holding Company, Inc.	(800) 804-1359	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	ADTH
29	Charles	Jordan	charles@adtheorent.com	AdTheorent Holding Company, Inc.	(800) 804-1359	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	ADTH
30	Kisa	Potok	lisa.potok@beamforall.com	Beam Global	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	BEEM
31	Desmond	Wheatley	desmond.wheatley@beamforall.com	Beam Global	+1 310 666 5111	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	BEEM
32	Richard	Little	rlittle@battalionoil.com	Battalion Oil Corporation	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	BATL
33	Kristen	McWatters	kmcwatters@battalionoil.com	Battalion Oil Corporation	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	BATL
34	Matt	Seele	msteele@battalionoil.com	Battalion Oil Corporation	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	BATL
35	Charles	Martin	cmartin@battalionoil.com	Battalion Oil Corporation	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	BATL
36	Daniel	Rohling	drohling@battalionoil.com	Battalion Oil Corporation	(281) 415-1806	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	BATL
37	Zachary	Venegas	zvenegas@helixtcs.com	Forian Inc.	(720) 328-5372	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	FORA
38	Scott	Ogur	sogur@helixtcs.com	Forian Inc.	(720) 328-5372	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	FORA
39	Mike	Vesey	mike.vesey@forian.com	Forian Inc.	(720) 328-5372	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	FORA
40	Max	Wygod	max.wygod@forian.com	Forian Inc.	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	FORA
41	Danielle	Barton	dan.barton@forian.com	Forian Inc.	(908) 824-3410	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	FORA
42	Drew	Chamberlain	drew.chamberlain@joann.com	JOANN Inc.	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	JOAN
43	Amanda	Hayes	amanda.hayes@joann.com	JOANN Inc.	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	JOAN
44	Ajay	Jain	ajay.jain@joann.com	JOANN Inc.	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	JOAN
45	Scott	Bibaud	sbibaud@atomera.com	Atomera Incorporated	(408) 442-5243	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	ATOM
46	Jotin	Marango	jmarango@ikenaoncology.com	Ikena Oncology, Inc.	(857) 273-8343	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	IKNA
47	Oscar	Iglesias	oscar.iglesias@codere.com	Codere Online Luxembourg, S.A.	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	CDRO
48	Moshe	Edree	moshe.edree@codere.com	Codere Online Luxembourg, S.A.	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	CDRO
49	Todd	Waltz	twaltz@aemetis.com	Aemetis, Inc.	(408) 213-0925	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	AMTX
50	Satya	Chillara	schillara@aemetis.com	Aemetis, Inc.	(408) 213-0940	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	AMTX
51	Eric	McAfee	emcafee@aemetis.com	Aemetis, Inc.	(408) 213-0925	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	AMTX
52	Hillary	Yaffe	hillary.yaffe@spire.com	Spire Global, Inc.	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	SPIR
53	Matt	Deines	matt.deines@ourfirstfed.com	First Northwest Bancorp	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	FNWB
54	Jennifer	Zaccardo	jennifer.zaccardo@ourfirstfed.com	First Northwest Bancorp	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	FNWB
55	Geri	Bullard	geri.bullard@ourfirstfed.com	First Northwest Bancorp	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	FNWB
56	Derek	Brown	derek.brown@ourfirstfed.com	First Northwest Bancorp	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	FNWB
57	Cindy	Finnie	cindy.finnie@ourfirstfed.com	First Northwest Bancorp	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	FNWB
58	Chris	Riffle	chris.riffle@ourfirstfed.com	First Northwest Bancorp	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	FNWB
59	Sheryl	Kinlaw	sheryl.kinlaw@citizensinc.com	Citizens, Inc.	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	CIA
60	Robert	Mauldin	robert.mauldin@citizensinc.com	Citizens, Inc.	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	CIA
61	Harvey	Waite	harvey.waite@citizensinc.com	Citizens, Inc.	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	CIA
62	Gerald	Shields	gerald.shields@citizensinc.com	Citizens, Inc.	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	CIA
63	Geert	Kersten	grkersten@cel-sci.com	CEL-SCI Corporation	(703) 506-9460	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	CVM
64	Gavin	de Windt	gdewindt@cel-sci.com	CEL-SCI Corporation	(703) 506-9460	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	CVM
65	Jason	Rando	jrando@tiberend.com	Anixa Biosciences, Inc.	(212) 375-2665	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	ANIX
66	Amit	Kumar, PhD	ak@anixa.com	Anixa Biosciences, Inc.	(408) 708-9802	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	ANIX
67	Crystal	Landsem	crystal@lulus.com	Lulu's Fashion Lounge Holdings, Inc.	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	LVLU
68	Andy	Wiederhorn	andy@fccgi.com	FAT Brands Inc.	(310) 402-0601	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	FAT
69	Kendall	Larsen	kendall_larsen@virnetx.com	VirnetX Holding Corp	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	VHC
70	Greg	Wood	greg_wood@virnetx.com	VirnetX Holding Corp	(775) 548-1769	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	VHC
71	Mike	Jaffa	mjaffa@gnusbrands.com	Genius Brands International, Inc.	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	GNUS
72	Andy	Heyward	aheyward@gnusbrands.com	Genius Brands International, Inc.	(310) 273-4222	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	GNUS
73	Scott	Dalgleish	scottdalgleish@theoncologyinstitute.com	The Oncology Institute, Inc.	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	TOI
74	Hilda	Agajanian	hagajanian@theoncologyinstitute.com	The Oncology Institute, Inc.	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	TOI
75	Daniel	Virnich	danielvirnich@theoncologyinstitute.com	The Oncology Institute, Inc.	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	TOI
76	Tiffanie	Horton	thorton@linkbancorp.com	LINKBANCORP, Inc.	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	LNKB
77	Kris	Paul	kpaul@linkbancorp.com	LINKBANCORP, Inc.	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	LNKB
78	Carl	Lundblad	clundblad@linkbancorp.com	LINKBANCORP, Inc.	(717)458-9095	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	LNKB
79	Andrew	Samuel	asamuel@linkbancorp.com	LINKBANCORP, Inc.	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	LNKB
80	Rebecca	Kuhn	rkuhn@neuropace.com	NeuroPace, Inc.	(650) 237-2700	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	NPCE
81	Michael	Favet	mfavet@neuropace.com	NeuroPace, Inc.	(650) 237-2700	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	NPCE
82	Randall	Fields	rfields@parkcitygroup.com	Park City Group, Inc.	(435) 645-2100	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	PCYG
83	Ron	Dutt	rdutt@fluxpower.com	Flux Power Holdings, Inc.	(877) 505-3589 , ext. 109	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	FLUX
84	Joshua	Samuels	copyconsultant@protonmail.com	Flux Power Holdings, Inc.	(321) 443-4121	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	FLUX
85	Chuck	Scheiwe	cscheiwe@fluxpower.com	Flux Power Holdings, Inc.	(877) 505-3589	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	FLUX
86	Laurence	Reid	lreid@decibeltx.com	Decibel Therapeutics, Inc.	(617) 370-8701	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	DBTX
87	Thomas	Wiggans	thomas.wiggans@pardesbio.com	Pardes Biosciences, Inc.	(415) 649-8758	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	PRDS
88	Heidi	Henson	heidi@pardesbio.com	Pardes Biosciences, Inc.	(617) 675-4060	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	PRDS
89	Stephanie	Corrente	scorrente@loopindustries.com	Loop Industries, Inc.	(450) 951-8555 ext. 226	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	LOOP
90	Nelson	Gentiletti	ngentiletti@loopindustries.com	Loop Industries, Inc.	(450) 951-8555	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	LOOP
91	Kevin	O'Dowd	kodowd@loopindustries.com	Loop Industries, Inc.	(450) 951-8555	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	LOOP
92	Drew	Hickey	dhickey@loopindustries.com	Loop Industries, Inc.	(450) 951-8555	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	LOOP
93	Daniel	Solomita	solomita@loopindustries.com	Loop Industries, Inc.	(450) 951-8555	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	LOOP
94	Sandra	Gardiner	sandra.gardiner@pulsebiosciences.com	Pulse Biosciences, Inc.	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	PLSE
95	Stewart	Kantor	stewart.kantor@ondas.com	Ondas Holdings Inc.	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	ONDS
96	Eric	Brock	eric.brock@ondas.com	Ondas Holdings Inc.	(888)350-9994	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	ONDS
97	Les	Goldman	lgoldman@nwbio.com	NWBO	301-656-9616	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	Referred by Kristen Shaughnessy
98	Dave	Innes	dinnes@nwbio.com	NWBO	804-513-4758	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	Referred by Kristen Shaughnessy
99	Dan	Bell	daniel.bell@dealmaker.tech	Deal Maker Transfer Agent	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	Naked Short Selling US Observer
100	Laura	Posner	lposner@cohenmilstein.com	Cohen Milstein	212.220.2925	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	Referred by Kristen Shaughnessy \n\nAttorney for NWBO spoofing case
101	Paul	Perito	andrewperito@hotmail.com	Star Scientific, Inc	301-346-1014	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	US Observer\nhttps://www.linkedin.com/in/paul-perito-20260629/
102	David	Michery	david@mullenusa.com	Mullen Automotive, Inc	562-298-6571	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	US Observer\nhttps://www.linkedin.com/in/david-michery-748a47a1/
103	Dan	Bates	danlbates@yahoo.com	Clean Vision Corporation	310-387-7636	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	US Observer\nhttps://www.linkedin.com/in/batesdan/
104	Dave	Mehalick	mpowerllc@yahoo.com	Coeptis Therapeutics Holdings, Inc	412-398-4112	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	US Observer\nhttps://www.linkedin.com/in/dave-mehalick-a5b80323/
105	Gregory	Poilasne	poilasne@hotmail.com	Nuvve Holding Corp	619-456-5161	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	Delivery has failed to these recipients or groups:\n\npoilasne@hotmail.com\nThe recipient's mailbox is full and can't accept messages now. Please try resending your message later, or contact the recipient directly.\n\n\nUS Observer\nhttps://www.linkedin.com/in/gregory-poilasne-68728b/
106	Gian Luca	Spriano	gspriano1@gmail.com	Micromobility.com Inc	914-255-1569	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	US Observer\nhttps://www.linkedin.com/in/gian-luca-spriano-283009a5/
107	Gabriel	René	grene1111@gmail.com	VERSES Technologies Inc	916-802-6129	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	US Observer\nhttps://www.linkedin.com/in/gabriel-ren%C3%A9-0201902/
108	Brendan	Jones	brendanseanjones@gmail.com	Blink Charging Co	703-872-7891	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	US Observer\nhttps://www.linkedin.com/in/brendansjones/
109	Martin	Shen	mjshen@me.com	FingerMotion, Inc	604-816-0788	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	US Observer\nhttps://www.linkedin.com/in/martin-j-shen-9b233717/?originalSubdomain=ca
110	Jacob	Cohen	jacob@mangorx.com	Mangoceuticals, Inc	214-242-9619	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	US Observer\nhttps://www.linkedin.com/in/jacob-cohen-ceo/
111	Ellery	Roberts	eroberts@1847holdings.com	\N	\N	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	\N
112	Wally	Klemp	wklemp@autonomix.com	Moleculin Biotech, Inc	713-305-5041	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	US Observer\nhttps://www.linkedin.com/company/moleculin-llc/
113	Chris	Kemp	chris@astra.com	Astra Space, Inc.	650-898-7783	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	US Observer\nhttps://www.linkedin.com/in/chrisckemp/
114	Diane	Garrett	diane.garrett@hycroftmining.com	Hycroft Mining Holding Corporation	775-304-0260	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	US Observer\nhttps://www.linkedin.com/in/diane-garrett-hycroft/
115	Michael	Pope	mikerpope@gmail.com	Focus Universal Inc	843-339-6637	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	US Observer\nhttps://www.linkedin.com/in/mikepope/
116	Donal	Carroll	dcarroll@fsdpharma.com	FSD Pharma Inc	416-854-8884	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	US Observer\nhttps://www.linkedin.com/in/donal-carroll-cpa-cma-19b0588/
117	Ellery	Roberts	eroberts@1847holdings.com	1847 Holdings LLC	310-492-4322	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	US Observer\nhttps://www.linkedin.com/in/elleryroberts/
118	Jaguar	Health	lconte@napopharma.com	Jaguar Health, Inc	650-616-1902	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	US Observer\nhttps://www.linkedin.com/in/lisa-conte-1941062/
119	Nikos	B	bardakisn@yahoo.gr	Cosmos Holdings d/b/a Cosmos Health, Inc	312-536-3102	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	US Observer\nhttps://www.linkedin.com/in/nikos-b-a448a71a/
120	John	Climaco	johnmclimaco@gmail.com	CNS Pharmaceuticals, Inc	801-699-7492	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	US Observer\nhttps://www.linkedin.com/in/john-climaco-62477a1/
121	Matthias	Aydt	matthias.aydt@googlemail.com	Faraday Future Intelligent Electric Inc	424-295-2767	\N	1	2025-02-17 23:27:12.001486-06	2025-02-17 23:27:12.001486-06	US Observer\nhttps://www.linkedin.com/in/matthias-aydt-aa67bb26/
\.


--
-- Data for Name: oauth_credentials; Type: TABLE DATA; Schema: public; Owner: suyashghimire
--

COPY public.oauth_credentials (id, credential_type, credentials_json, created_at, updated_at) FROM stdin;
13	token	{"token": "ya29.a0AXeO80QyNq4VdANPVvhpHFCSYpBLBPVDfwF1nDMLlFlUeHqNgT49zlzeOQxsRKWhHPm7C6BKAeu-mUi0Cbv-XW0kj-vjs2z_kmiP7uyJB1zqVTlGaxANYsxoZIPw97l2TltZNVUrDncEs2UxC5M0CQBhWp-AAGBvjCh8E64N-gaCgYKAdYSARISFQHGX2Mi8rFji1xVJYVLan_hErROrQ0177", "refresh_token": "1//04cvxzUBK23oFCgYIARAAGAQSNwF-L9Ir8cZg8Si56qy5NDjyFM2CYY3CbQgbdh-70f4JuPpNAZ8WLcXdoKmzr7OW8BENgzuCR7E", "token_uri": "https://oauth2.googleapis.com/token", "client_id": "728984450065-tp35h42l0i3va2543li21amv8rqcru6g.apps.googleusercontent.com", "client_secret": "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", "scopes": ["https://www.googleapis.com/auth/gmail.send"], "expiry": "2025-02-18T06:33:59.274836"}	2025-02-17 23:34:00.278102-06	2025-02-17 23:34:00.278107-06
1	client_secret	{"web":{"client_id":"105157187942-89ha5k01sv2ajtqqc834or657821ajm3.apps.googleusercontent.com","project_id":"skilful-bearing-450622-r1","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"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","redirect_uris":["http://localhost:8000/oauth2callback","http://127.0.0.1:8000/oauth2callback","http://localhost:8000/auth/callback"],"javascript_origins":["http://localhost:8000","http://127.0.0.1:8000"]}}	2025-02-12 22:11:24.153216-06	2025-02-12 22:11:24.153216-06
\.


--
-- Data for Name: sequence_mapping; Type: TABLE DATA; Schema: public; Owner: suyashghimire
--

COPY public.sequence_mapping (sequence_id, email_body, article_link, is_active, email_subject) FROM stdin;
6	<p>I wanted to personally bring to your attention an article I recently wrote regarding the SEC's extension of the compliance date for short sale reporting and its implications for issuers and shareholders. This delay creates an opportunity for immediate action, and the US~Observer is prepared to expose manipulative trading practices that continue to harm businesses and investors.</p><ul><li>Through investigative journalism, we can uncover and correct these wrongdoings, ensuring transparency and accountability in financial markets. I believe this is a critical issue that warrants your attention, and I would appreciate the opportunity to discuss how we can address it in your company effectively.</li></ul><p><br></p>	https://usobserver.com/who-is-guarding-the-hen-house/	f	Who is guarding the hen house
15	<p>I wanted to personally bring to your attention an article I recently wrote regarding the SEC's extension of the compliance date for short sale reporting and its implications for issuers and shareholders. This delay creates an opportunity for immediate action, and the US~Observer is prepared to expose manipulative trading practices that continue to harm businesses and investors.</p><p>Through investigative journalism, we can uncover and correct these wrongdoings, ensuring transparency and accountability in financial markets. I believe this is a critical issue that warrants your attention, and I would appreciate the opportunity to discuss how we can address it in your company effectively.</p>	https://usobserver.com/exposing-naked-shorts-obtaining-justice-and-shareholder-protection/	t	SEC's extension of the compliance date for short sale
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

SELECT pg_catalog.setval('public.email_metrics_id_seq', 13, true);


--
-- Name: mailing_list_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: suyashghimire
--

SELECT pg_catalog.setval('public.mailing_list_user_id_seq', 186, true);


--
-- Name: mailing_list_user_id_seq1; Type: SEQUENCE SET; Schema: public; Owner: suyashghimire
--

SELECT pg_catalog.setval('public.mailing_list_user_id_seq1', 123, true);


--
-- Name: oauth_credentials_id_seq; Type: SEQUENCE SET; Schema: public; Owner: suyashghimire
--

SELECT pg_catalog.setval('public.oauth_credentials_id_seq', 13, true);


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
    ADD CONSTRAINT email_metrics_contact_id_fkey FOREIGN KEY (contact_id) REFERENCES public.mailing_list(user_id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

