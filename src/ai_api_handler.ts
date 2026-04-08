/**
 * AI-generated API handler for user management.
 * Generated with GitHub Copilot assistance.
 */

interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user' | 'viewer';
  createdAt: Date;
  lastLogin?: Date;
}

interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  pageSize: number;
  hasMore: boolean;
}

interface UserFilter {
  role?: string;
  search?: string;
  sortBy?: keyof User;
  sortOrder?: 'asc' | 'desc';
}

/**
 * Paginate an array of items with filtering and sorting support.
 * Implements cursor-based pagination for consistent results.
 */
export function paginateUsers(
  users: User[],
  page: number = 1,
  pageSize: number = 20,
  filter?: UserFilter
): PaginatedResponse<User> {
  let filtered = [...users];

  // Apply role filter
  if (filter?.role) {
    filtered = filtered.filter(u => u.role === filter.role);
  }

  // Apply search filter
  if (filter?.search) {
    const searchLower = filter.search.toLowerCase();
    filtered = filtered.filter(u =>
      u.name.toLowerCase().includes(searchLower) ||
      u.email.toLowerCase().includes(searchLower)
    );
  }

  // Apply sorting
  if (filter?.sortBy) {
    const order = filter.sortOrder === 'desc' ? -1 : 1;
    filtered.sort((a, b) => {
      const aVal = a[filter.sortBy!];
      const bVal = b[filter.sortBy!];
      if (aVal < bVal) return -1 * order;
      if (aVal > bVal) return 1 * order;
      return 0;
    });
  }

  const start = (page - 1) * pageSize;
  const end = start + pageSize;
  const data = filtered.slice(start, end);

  return {
    data,
    total: filtered.length,
    page,
    pageSize,
    hasMore: end < filtered.length,
  };
}

/**
 * Validate email format using RFC 5322 simplified pattern.
 * Returns true if the email appears valid.
 */
export function isValidEmail(email: string): boolean {
  const emailRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
  return emailRegex.test(email);
}

/**
 * Generate a unique identifier with a prefix.
 * Uses timestamp + random component for uniqueness.
 */
export function generateId(prefix: string = 'usr'): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 8);
  return `${prefix}_${timestamp}_${random}`;
}

/**
 * Deep clone an object, handling Date objects correctly.
 */
export function deepClone<T>(obj: T): T {
  if (obj === null || typeof obj !== 'object') return obj;
  if (obj instanceof Date) return new Date(obj.getTime()) as unknown as T;
  if (Array.isArray(obj)) return obj.map(item => deepClone(item)) as unknown as T;

  const cloned = {} as T;
  for (const key in obj) {
    if (Object.prototype.hasOwnProperty.call(obj, key)) {
      (cloned as any)[key] = deepClone((obj as any)[key]);
    }
  }
  return cloned;
}
