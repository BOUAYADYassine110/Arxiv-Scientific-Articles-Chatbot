import axios from 'axios';
import { SearchRequest, SearchResponse, Stats } from '../types';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const searchArticles = async (request: SearchRequest): Promise<SearchResponse> => {
  try {
    const response = await api.post('/search', request);
    return response.data as SearchResponse;
  } catch (error: any) {
    if (error.response) {
      throw new Error(`Search failed: ${error.response.data?.detail || error.message}`);
    }
    throw new Error('Search request failed');
  }
};

export const getStats = async (): Promise<Stats> => {
  try {
    const response = await api.get('/stats');
    return response.data as Stats;
  } catch (error: any) {
    if (error.response) {
      throw new Error(`Failed to fetch stats: ${error.response.data?.detail || error.message}`);
    }
    throw new Error('Stats request failed');
  }
};

export const getYears = async (): Promise<string[]> => {
  try {
    const response = await api.get('/years');
    return (response.data as any).years;
  } catch (error: any) {
    if (error.response) {
      throw new Error(`Failed to fetch years: ${error.response.data?.detail || error.message}`);
    }
    throw new Error('Years request failed');
  }
};