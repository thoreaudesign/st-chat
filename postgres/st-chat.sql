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

--
-- Name: action; Type: TYPE; Schema: public; Owner: st-chat
--

CREATE TYPE public.action AS ENUM (
    'join',
    'message',
    'exit'
);


ALTER TYPE public.action OWNER TO "st-chat";

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: chat_log; Type: TABLE; Schema: public; Owner: st-chat
--

CREATE TABLE public.chat_log (
    "timestamp" character varying(16),
    action public.action,
    message text
);


ALTER TABLE public.chat_log OWNER TO "st-chat";

--
-- Name: execution; Type: TABLE; Schema: public; Owner: st-chat
--

CREATE TABLE public.execution (
    "timestamp" character varying(16),
    symbol character varying(255),
    market character varying(64),
    price character varying(32),
    quantity character varying(32),
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
-- PostgreSQL database dump complete
--

