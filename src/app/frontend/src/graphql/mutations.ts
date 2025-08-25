import { gql } from '@apollo/client/core'

// Мутации для организаций
export const CREATE_ORGANIZATION = gql`
  mutation CreateOrganization($input: CreateOrganizationInput!) {
    createOrganization(input: $input) {
      id
      name
      type
      description
      foundedDate
      dissolvedDate
      location {
        id
        name
      }
      parentOrganization {
        id
        name
      }
      createdAt
      updatedAt
    }
  }
`

export const UPDATE_ORGANIZATION = gql`
  mutation UpdateOrganization($id: ID!, $input: UpdateOrganizationInput!) {
    updateOrganization(id: $id, input: $input) {
      id
      name
      type
      description
      foundedDate
      dissolvedDate
      location {
        id
        name
      }
      parentOrganization {
        id
        name
      }
      updatedAt
    }
  }
`

export const DELETE_ORGANIZATION = gql`
  mutation DeleteOrganization($id: ID!) {
    deleteOrganization(id: $id) {
      id
      name
    }
  }
`

// Мутации для государств
export const CREATE_STATE = gql`
  mutation CreateState($input: CreateStateInput!) {
    createState(input: $input) {
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
      }
      createdAt
      updatedAt
    }
  }
`

export const UPDATE_STATE = gql`
  mutation UpdateState($id: ID!, $input: UpdateStateInput!) {
    updateState(id: $id, input: $input) {
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
      }
      updatedAt
    }
  }
`

export const DELETE_STATE = gql`
  mutation DeleteState($id: ID!) {
    deleteState(id: $id) {
      id
      name
    }
  }
`

// Мутации для людей
export const CREATE_PERSON = gql`
  mutation CreatePerson($input: CreatePersonInput!) {
    createPerson(input: $input) {
      id
      firstName
      lastName
      middleName
      birthDate
      deathDate
      biography
      createdAt
      updatedAt
    }
  }
`

export const UPDATE_PERSON = gql`
  mutation UpdatePerson($id: ID!, $input: UpdatePersonInput!) {
    updatePerson(id: $id, input: $input) {
      id
      firstName
      lastName
      middleName
      birthDate
      deathDate
      biography
      updatedAt
    }
  }
`

export const DELETE_PERSON = gql`
  mutation DeletePerson($id: ID!) {
    deletePerson(id: $id) {
      id
      firstName
      lastName
    }
  }
`

// Мутации для мест
export const CREATE_LOCATION = gql`
  mutation CreateLocation($input: CreateLocationInput!) {
    createLocation(input: $input) {
      id
      name
      type
      latitude
      longitude
      parentLocation {
        id
        name
      }
      createdAt
      updatedAt
    }
  }
`

export const UPDATE_LOCATION = gql`
  mutation UpdateLocation($id: ID!, $input: UpdateLocationInput!) {
    updateLocation(id: $id, input: $input) {
      id
      name
      type
      latitude
      longitude
      parentLocation {
        id
        name
      }
      updatedAt
    }
  }
`

export const DELETE_LOCATION = gql`
  mutation DeleteLocation($id: ID!) {
    deleteLocation(id: $id) {
      id
      name
    }
  }
`