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
  name: string
  birthDate?: string
  deathDate?: string
  nationality?: string
  isFictional?: boolean
  historicalPeriod?: HistoricalPeriod
  positions?: Position[]
  createdAt: string
  updatedAt: string
}

export interface HistoricalPeriod {
  id: string
  name: string
  startDate?: string
  endDate?: string
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

// Типы для связанных данных
export interface OrganizationWithPositions {
  id: string
  name: string
  positions: Position[]
}

export interface OrganizationWithChildren {
  id: string
  name: string
  childUnits: Organization[]
}

export interface PersonPosition {
  id: string
  person: Person
  position: Position
  startDate: string
  endDate?: string
  appointmentType: string
  source: string
}

export enum PositionHierarchy {
  ENTRY = 'ENTRY',
  JUNIOR = 'JUNIOR',
  MIDDLE = 'MIDDLE',
  SENIOR = 'SENIOR',
  LEAD = 'LEAD',
  MANAGER = 'MANAGER',
  DIRECTOR = 'DIRECTOR',
  EXECUTIVE = 'EXECUTIVE'
}

export enum AppointmentType {
  FULL_TIME = 'FULL_TIME',
  PART_TIME = 'PART_TIME',
  CONTRACT = 'CONTRACT',
  TEMPORARY = 'TEMPORARY',
  INTERNSHIP = 'INTERNSHIP'
}