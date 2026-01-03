const API_BASE = '/api';

interface LoginCredentials {
    username: string;
    password: string;
}

interface RegisterData {
    email: string;
    password: string;
    body_weight?: number;
    age?: number;
    gender?: string;
    vo2max?: number;
}

interface TokenResponse {
    access_token: string;
    token_type: string;
}

interface UserResponse {
    id: number;
    email: string;
    body_weight?: number;
    age?: number;
    gender?: string;
    vo2max?: number;
    created_at: string;
}

interface UploadMetadata {
    session_type?: string;
    race_name?: string;
    notes?: string;
    fatigue_level?: number;
    general_sensation?: number;
    sleep_quality?: number;
    hydration_status?: string;
    weather_condition?: string;
    trail_condition?: string;
}

interface UploadResponse {
    id: number;
    filename: string;
    filepath: string;
    upload_date: string;
    session_type?: string;
    race_name?: string;
    notes?: string;
    fatigue_level?: number;
    general_sensation?: number;
    sleep_quality?: number;
    hydration_status?: string;
    weather_condition?: string;
    trail_condition?: string;
}

class ApiClient {
    private token: string | null = null;

    constructor() {
        if (typeof window !== 'undefined') {
            this.token = localStorage.getItem('token');
        }
    }

    setToken(token: string) {
        this.token = token;
        if (typeof window !== 'undefined') {
            localStorage.setItem('token', token);
        }
    }

    clearToken() {
        this.token = null;
        if (typeof window !== 'undefined') {
            localStorage.removeItem('token');
        }
    }

    getToken(): string | null {
        return this.token;
    }

    isAuthenticated(): boolean {
        return this.token !== null;
    }

    private getHeaders(includeAuth: boolean = false): HeadersInit {
        const headers: HeadersInit = {
            'Content-Type': 'application/json',
        };
        if (includeAuth && this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }
        return headers;
    }

    async register(data: RegisterData): Promise<UserResponse> {
        const response = await fetch(`${API_BASE}/users/register`, {
            method: 'POST',
            headers: this.getHeaders(),
            body: JSON.stringify(data),
        });
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Registration failed');
        }
        return response.json();
    }

    async login(credentials: LoginCredentials): Promise<TokenResponse> {
        const formData = new FormData();
        formData.append('username', credentials.username);
        formData.append('password', credentials.password);

        const response = await fetch(`${API_BASE}/users/login`, {
            method: 'POST',
            body: formData,
        });
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Login failed');
        }
        const data = await response.json();
        this.setToken(data.access_token);
        return data;
    }

    logout() {
        this.clearToken();
    }

    async uploadFile(file: File, metadata: UploadMetadata): Promise<UploadResponse> {
        const formData = new FormData();
        formData.append('file', file);

        Object.entries(metadata).forEach(([key, value]) => {
            if (value !== undefined && value !== null) {
                formData.append(key, String(value));
            }
        });

        const response = await fetch(`${API_BASE}/upload/`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.token}`,
            },
            body: formData,
        });
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Upload failed');
        }
        return response.json();
    }

    async listUploads(): Promise<UploadResponse[]> {
        const response = await fetch(`${API_BASE}/upload/`, {
            headers: {
                'Authorization': `Bearer ${this.token}`,
            },
        });
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to fetch uploads');
        }
        return response.json();
    }
}

export const api = new ApiClient();
export type { RegisterData, LoginCredentials, TokenResponse, UserResponse, UploadMetadata, UploadResponse };
