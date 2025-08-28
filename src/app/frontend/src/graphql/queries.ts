import { gql } from '@apollo/client/core'

// Запросы для организаций
export const GET_ORGANIZATIONS = gql`
  query GetOrganizations {
    organizationalUnits {
      id
      name
      type
      foundedDate
      dissolvedDate
      isFictional
    }
  }
`

// Запрос для получения должностей организации
export const GET_ORGANIZATION_POSITIONS = gql`
  query GetOrganizationPositions {
    positions {
      id
      title
      createdDate
      abolishedDate
      hierarchy
      responsibilities
      isActive
      organization {
        id
        name
      }
    }
  }
`

// Запрос для получения дочерних организаций
export const GET_CHILD_ORGANIZATIONS = gql`
  query GetChildOrganizations {
    organizationalUnits {
      id
      name
      type
      foundedDate
      dissolvedDate
      isFictional
    }
  }
`

export const GET_ORGANIZATION = gql`
  query GetOrganization($id: ID!) {
    organization(id: $id) {
      id
      name
      type
      description
      foundedDate
      dissolvedDate
      location {
        id
        name
        type
        latitude
        longitude
      }
      parentOrganization {
        id
        name
        type
      }
      childOrganizations {
        id
        name
        type
      }
      positions {
        id
        title
        description
        startDate
        endDate
        isActive
        person {
          id
          firstName
          lastName
          middleName
        }
      }
      createdAt
      updatedAt
    }
  }
`

// Запросы для государств
export const GET_STATES = gql`
  query GetStates($search: SearchInput) {
    states(search: $search) {
      id
      name
      code
      type
      description
      foundedDate
      dissolvedDate
      capital {
        id
        name
        type
      }
      territory {
        id
        name
        type
      }
      organizations {
        id
        name
        type
      }
      createdAt
      updatedAt
    }
  }
`

// Запросы для людей
export const GET_PEOPLE = gql`
  query GetPeople($search: SearchInput) {
    people(search: $search) {
      id
      name
      birthDate
      deathDate
      nationality
      isFictional
      historicalPeriod {
        id
        name
        startDate
        endDate
      }
      positions {
        id
        title
        organization {
          id
          name
          type
        }
        startDate
        endDate
        isActive
      }
      createdAt
      updatedAt
    }
  }
`

// Запросы для мест
export const GET_LOCATIONS = gql`
  query GetLocations($search: SearchInput) {
    locations(search: $search) {
      id
      name
      type
      latitude
      longitude
      parentLocation {
        id
        name
        type
      }
      childLocations {
        id
        name
        type
      }
      organizations {
        id
        name
        type
      }
      createdAt
      updatedAt
    }
  }
`