--
-- PostgreSQL database dump
--

-- Dumped from database version 13.1
-- Dumped by pg_dump version 13.1

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
-- Name: execution; Type: TABLE; Schema: public; Owner: st-chat
--

CREATE TABLE public.execution (
    "timestamp" character varying(16),
    symbol character varying(255),
    market character varying(64),
    price character varying(32),
    executionepoch character varying(16),
    statesymbol character varying(2)
);


ALTER TABLE public.execution OWNER TO "st-chat";

--
-- Name: sport_event; Type: TABLE; Schema: public; Owner: st-chat
--

CREATE TABLE public.sport_event (
    "timestamp" integer,
    sport character varying(64),
    match_title text,
    data_event text
);


ALTER TABLE public.sport_event OWNER TO "st-chat";

--
-- Data for Name: execution; Type: TABLE DATA; Schema: public; Owner: st-chat
--

COPY public.execution ("timestamp", symbol, market, price, executionepoch, statesymbol) FROM stdin;
\.


--
-- Data for Name: sport_event; Type: TABLE DATA; Schema: public; Owner: st-chat
--

COPY public.sport_event ("timestamp", sport, match_title, data_event) FROM stdin;
\.


--
-- PostgreSQL database dump complete
--

