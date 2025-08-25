// GraphQL входные типы для Vuege

export interface CreateOrganizationInput {
  name: string
  type: string
  description?: string
  foundedDate?: string
  dissolvedDate?: string
  locationId?: string
  parentOrganizationId?: string
}

export interface UpdateOrganizationInput {
  name?: string
  type?: string
  description?: string
  foundedDate?: string
  dissolvedDate?: string
  locationId?: string
  parentOrganizationId?: string
}

export interface CreateStateInput {
  name: string
  code?: string
  type: string
  description?: string
  foundedDate?: string
  dissolvedDate?: string
  capitalId?: string
}

export interface UpdateStateInput {
  name?: string
  code?: string
  type?: string
  description?: string
  foundedDate?: string
  dissolvedDate?: string
  capitalId?: string
}

export interface CreatePersonInput {
  firstName: string
  lastName: string
  middleName?: string
  birthDate?: string
  deathDate?: string
  biography?: string
}

export interface UpdatePersonInput {
  firstName?: string
  lastName?: string
  middleName?: string
  birthDate?: string
  deathDate?: string
  biography?: string
}

export interface CreateLocationInput {
  name: string
  type: string
  latitude?: number
  longitude?: number
  parentLocationId?: string
}

export interface UpdateLocationInput {
  name?: string
  type?: string
  latitude?: number
  longitude?: number
  parentLocationId?: string
}

export interface CreatePositionInput {
  title: string
  description?: string
  organizationId: string
  personId?: string
  startDate?: string
  endDate?: string
  isActive: boolean
}

export interface UpdatePositionInput {
  title?: string
  description?: string
  organizationId?: string
  personId?: string
  startDate?: string
  endDate?: string
  isActive?: boolean
}