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
  const disciplineCompetences = ref([])
  const editingDiscipline = ref(null)
  const saving = ref(false)
  
  // Фильтры
  const textFilter = ref('')
  const groupTextFilter = ref('')
  const statusFilter = ref('')
  const myFilter = ref(0)
  const currentPlanId = ref(null)

  // Валидация матрицы
  const matrixValidation = ref({
    isValid: false,
    disciplinesWithoutCompetences: [],
    competencesWithoutDisciplines: [],
    lastChecked: null,
    validationInProgress: false
  })

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

  async function fetchDisciplineCompetencesDetailed(planId, disciplineId) {
    loading.value = true
    try {
      if (!planId || !disciplineId) {
        throw new Error('Plan ID and Discipline ID are required')
      }
      
      const response = await api.get('/api/competence/discipline-competences-detailed/', {
        params: { 
          plan_id: planId,
          discipline_id: disciplineId
        }
      })
      
      disciplineCompetences.value = response.data.competences
      editingDiscipline.value = {
        id: response.data.discipline_id,
        index: response.data.discipline_index,
        name: response.data.discipline_name,
        planId: response.data.plan_mira_id
      }
      
      return response.data
    } catch (error) {
      console.error('Error fetching detailed discipline competences:', error)
      throw error
    } finally {
      loading.value = false
    }
  }
  
  async function updateDisciplineCompetences(selectedCompetences) {
    saving.value = true
    try {
      if (!editingDiscipline.value) {
        throw new Error('No discipline selected for editing')
      }
      
      const payload = {
        plan_id: editingDiscipline.value.planId,
        discipline_id: editingDiscipline.value.id,
        selected_competences: selectedCompetences  
      }
      
      const response = await api.post(
        '/api/competence/update-discipline-competences/', 
        payload
      )
      
      matrixValidation.value.isValid = false
      
      await fetchCompetenceMatrix(editingDiscipline.value.planId)
      
      return response.data
    } catch (error) {
      console.error('Error updating discipline competences:', error)
      throw error
    } finally {
      saving.value = false
    }
  }
  
  function clearEditingDiscipline() {
    editingDiscipline.value = null
    disciplineCompetences.value = []
  }

  // ВВалидация матрицы
  async function validateCompetenceMatrix(planId) {
    matrixValidation.value.validationInProgress = true
    
    try {
      if (!planId) {
        if (!currentPlanId.value) {
          throw new Error('Plan ID is required for validation')
        }
        planId = currentPlanId.value
      }
      
      // 1. Загружаем матрицу компетенций
      if (!competenceMatrix.value.length) {
        await fetchCompetenceMatrix(planId)
      }
      
      // 2. Загружаем все компетенции плана
      const competencesData = await fetchAllCompetences(planId)
      const allCompetences = competencesData.competences || []
      
      // 3. Находим дисциплины без компетенций
      const disciplines = competenceMatrix.value.filter(
        item => item.type === 'discipline'
      )
      
      const disciplinesWithoutCompetences = disciplines.filter(
        disc => !disc.competence_indices || disc.competence_indices.trim() === ''
      ).map(disc => ({
        index: disc.index,
        name: disc.name
      }))
      
      // 4. Находим все компетенции, которые есть в матрице
      const usedCompetences = new Set()
      competenceMatrix.value.forEach(item => {
        if (item.competence_indices) {
          item.competence_indices.split(', ').forEach(comp => {
            usedCompetences.add(comp.trim())
          })
        }
      })
      
      // 5. Находим компетенции без дисциплин
      const competencesWithoutDisciplines = allCompetences.filter(
        comp => !usedCompetences.has(comp.competence_index)
      ).map(comp => ({
        competence_index: comp.competence_index,
        competence: comp.competence
      }))
      
      // 6. Проверяем валидность
      const isValid = disciplinesWithoutCompetences.length === 0 && 
                     competencesWithoutDisciplines.length === 0
      
      // 7. Сохраняем результаты валидации
      matrixValidation.value = {
        isValid,
        disciplinesWithoutCompetences,
        competencesWithoutDisciplines,
        lastChecked: new Date(),
        validationInProgress: false
      }
      
      // 8. Сохраняем для других страниц
      localStorage.setItem(`matrix_valid_${planId}`, isValid ? 'true' : 'false')
      
      if (isValid) {
        localStorage.setItem(`matrix_validation_${planId}`, JSON.stringify({
          isValid,
          checkedAt: new Date().toISOString()
        }))
      }
      
      return matrixValidation.value
      
    } catch (error) {
      console.error('Error validating competence matrix:', error)
      matrixValidation.value.validationInProgress = false
      throw error
    }
  }
  
  // Проверка валидности 
  function checkMatrixValidityFromStorage(planId) {
    if (!planId) planId = currentPlanId.value
    if (!planId) return false
    
    const storedValue = localStorage.getItem(`matrix_valid_${planId}`)
    return storedValue === 'true'
  }
  
  function resetMatrixValidation() {
    matrixValidation.value = {
      isValid: false,
      disciplinesWithoutCompetences: [],
      competencesWithoutDisciplines: [],
      lastChecked: null,
      validationInProgress: false
    }
    
    if (currentPlanId.value) {
      localStorage.removeItem(`matrix_valid_${currentPlanId.value}`)
      localStorage.removeItem(`matrix_validation_${currentPlanId.value}`)
    }
  }
  
  function getValidationStatus() {
    return {
      ...matrixValidation.value,
      fromStorage: currentPlanId.value ? 
        checkMatrixValidityFromStorage(currentPlanId.value) : false
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
    disciplineCompetences,
    editingDiscipline,
    saving,
    fetchDisciplineCompetencesDetailed,
    updateDisciplineCompetences,
    clearEditingDiscipline,
    currentPlanDisciplines,

    matrixValidation,
    validateCompetenceMatrix,
    checkMatrixValidityFromStorage,
    resetMatrixValidation,
    getValidationStatus
  }
})