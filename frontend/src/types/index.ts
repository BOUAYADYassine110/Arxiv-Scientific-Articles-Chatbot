export interface Article {
  id: number;
  title: string;
  abstract: string;
  published: string;
  categories: string;
  authors?: string;
}

export interface SearchRequest {
  query: string;
  year_filter?: string;
  category_filter?: string;
  author_filter?: string;
  title_filter?: string;
  abstract_filter?: string;
  search_type: 'manual' | 'ai';
  limit?: number;
}

export interface SearchResponse {
  articles: Article[];
  total_count: number;
  search_type: string;
  explanation?: string;
}

export interface Stats {
  total_papers: number;
  latest_year: string;
  year_span: number;
  papers_by_year: Record<string, number>;
}