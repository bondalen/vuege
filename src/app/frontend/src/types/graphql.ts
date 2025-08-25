// GraphQL типы для Vuege

export interface Organization {
  id: string
  name: string
  type: OrganizationType
  description?: string
  foundedDate?: string
  dissolvedDate?: string
  location?: Location
  parentOrganization?: Organization
  childOrganizations?: Organization[]
  positions?: Position[]
  createdAt: string
  updatedAt: string
}

export interface Position {
  id: string
  title: string
  description?: string
  organization: Organization
  person?: Person
  startDate?: string
  endDate?: string
  isActive: boolean
  createdAt: string
  updatedAt: string
}

export interface Person {
  id: string
  firstName: string
  lastName: string
  middleName?: string
  birthDate?: string
  deathDate?: string
  biography?: string
  positions?: Position[]
  createdAt: string
  updatedAt: string
}

export interface Location {
  id: string
  name: string
  type: LocationType
  latitude?: number
  longitude?: number
  parentLocation?: Location
  childLocations?: Location[]
  organizations?: Organization[]
  createdAt: string
  updatedAt: string
}

export interface State {
  id: string
  name: string
  code?: string
  type: StateType
  description?: string
  foundedDate?: string
  dissolvedDate?: string
  capital?: Location
  territory?: Location[]
  organizations?: Organization[]
  createdAt: string
  updatedAt: string
}

export enum OrganizationType {
  GOVERNMENT = 'GOVERNMENT',
  COMMERCIAL = 'COMMERCIAL',
  NON_PROFIT = 'NON_PROFIT',
  EDUCATIONAL = 'EDUCATIONAL',
  MILITARY = 'MILITARY',
  RELIGIOUS = 'RELIGIOUS',
  OTHER = 'OTHER'
}

export enum LocationType {
  COUNTRY = 'COUNTRY',
  REGION = 'REGION',
  CITY = 'CITY',
  DISTRICT = 'DISTRICT',
  ADDRESS = 'ADDRESS',
  COORDINATES = 'COORDINATES'
}

export enum StateType {
  EMPIRE = 'EMPIRE',
  KINGDOM = 'KINGDOM',
  REPUBLIC = 'REPUBLIC',
  FEDERATION = 'FEDERATION',
  CONFEDERATION = 'CONFEDERATION',
  OTHER = 'OTHER'
}

export interface PaginationInput {
  page: number
  size: number
}

export interface SearchInput {
  query: string
  filters?: Record<string, any>
  pagination?: PaginationInput
}

export interface GraphQLResponse<T> {
  data?: T
  errors?: Array<{
    message: string
    locations?: Array<{
      line: number
      column: number
    }>
    path?: string[]
  }>
}