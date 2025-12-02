import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from 'boot/axios'
import _ from 'lodash'

export const useCompetencePassportStore = defineStore('competencePassport', () => {
  const programList = ref([])
  const groupsList = ref([])
  const currentProgram = ref(null)
  const currentGroupPrograms = ref([])
  const currentPlanCompetences = ref([])
  const loading = ref(false)
  const selectedYear = ref(new Date().getFullYear())
  const currentPlanDisciplines = ref([])
  const competenceMatrix = ref([])
  const matrixLoading = ref(false)
  
  // Фильтры
  const textFilter = ref('')
  const groupTextFilter = ref('')
  const statusFilter = ref('')
  const myFilter = ref(0)
  const currentPlanId = ref(null)

  // Геттеры
  const filteredPrograms = computed(() => {
    return _.orderBy(programList.value, ['abbrprofile', 'startyear'])
  })
  
  const filteredGroupPrograms = computed(() => {
    let txtFilter = textFilter.value.trim().toLowerCase();
    return _(currentGroupPrograms.value)
      .filter(x => {
        return (myFilter.value == 0 || x.type.includes('person'))
          && ((txtFilter == '' || x.discode.toLowerCase().includes(txtFilter))
            || (txtFilter == '' || x.discpl.toLowerCase().includes(txtFilter))
            || (txtFilter == '' || x.razrab_name.toLowerCase().includes(txtFilter)))
          && (!statusFilter.value || x.status_verbose == statusFilter.value)
      })
      .value()
  })

  // Действия
  async function fetchGroupsList() {
    loading.value = true
    try {
      const params = {
        year: selectedYear.value,
        text: textFilter.value,
        groupText: groupTextFilter.value,
        status: statusFilter.value,
        my: myFilter.value
      }
      
      const response = await api.get('/api/competence/group-list/', { params })
      groupsList.value = response.data
    } catch (error) {
      console.error('Error fetching groups list:', error)
      groupsList.value = []
      throw error
    } finally {
      loading.value = false
    }
  }

  async function fetchGroupPrograms(planId) {
    loading.value = true
    try {
      currentPlanId.value = planId
      const response = await api.get(`/api/competence/${planId}/group-program/`)
      currentGroupPrograms.value = response.data
    } catch (error) {
      console.error('Error fetching group programs:', error)
      currentGroupPrograms.value = []
      throw error
    } finally {
      loading.value = false
    }
  }

  function setCurrentProgram(program) {
    currentProgram.value = program
  }
  
  async function getProgramDetail(programId) {
    try {
      const response = await api.get(`/api/competence/${programId}/`)
      return response.data
    } catch (error) {
      console.error('Error fetching program detail:', error)
      throw error
    }
  }

  async function fetchAllCompetences(planId) {
    loading.value = true
    try {
      if (!planId) {
        throw new Error('Plan ID is required')
      }
      
      const response = await api.get('/api/competence/all-competences/', {
        params: { plan_id: planId }
      })
      currentPlanCompetences.value = response.data.competences
      return response.data
    } catch (error) {
      console.error('Error fetching plan competences:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  async function fetchAllDisciplines(planId) {
    loading.value = true
    try {
      if (!planId) {
        throw new Error('Plan ID is required')
      }
      
      const response = await api.get('/api/competence/all-disciplines/', {
        params: { plan_id: planId }
      })
      currentPlanDisciplines.value = response.data.disciplines
      return response.data
    } catch (error) {
      console.error('Error fetching plan disciplines:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  async function fetchCompetenceMatrix(planId) {
    matrixLoading.value = true
    try {
      if (!planId) {
        throw new Error('Plan ID is required')
      }
      
      const response = await api.get('/api/competence/competence-matrix/', {
        params: { plan_id: planId }
      })
      competenceMatrix.value = response.data.matrix || []
      return response.data
    } catch (error) {
      console.error('Error fetching competence matrix:', error)
      throw error
    } finally {
      matrixLoading.value = false
    }
  }

  return {
    programList,
    groupsList,
    currentProgram,
    currentGroupPrograms,
    loading,
    selectedYear,
    textFilter,
    groupTextFilter,
    statusFilter,
    myFilter,
    currentPlanId,
    filteredPrograms,
    filteredGroupPrograms,
    fetchGroupsList,
    fetchGroupPrograms,
    setCurrentProgram,
    getProgramDetail,
    fetchAllCompetences,
    fetchAllDisciplines,
    competenceMatrix,
    matrixLoading,
    fetchCompetenceMatrix,
  }
})