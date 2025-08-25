import { gql } from '@apollo/client/core'

// Запросы для организаций
export const GET_ORGANIZATIONS = gql`
  query GetOrganizations($search: SearchInput) {
    organizations(search: $search) {
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
      }
      parentOrganization {
        id
        name
      }
      childOrganizations {
        id
        name
      }
      positions {
        id
        title
        person {
          id
          firstName
          lastName
        }
      }
      createdAt
      updatedAt
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
      firstName
      lastName
      middleName
      birthDate
      deathDate
      biography
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