import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from 'boot/axios'
import _ from 'lodash'
import { LocalStorage, useQuasar } from 'quasar';

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
  const schemaData = ref([])
  const schemaLoading = ref(false)
  
  // Фильтры
  const textFilter = ref('')
  const groupTextFilter = ref('')
  const statusFilter = ref('')
  const myFilter = ref(0)
  const currentPlanId =  ref(LocalStorage.getItem('current_plan_id') || null)

  // Валидация матрицы
  const matrixValidation = ref({
    isValid: false,
    disciplinesWithoutCompetences: [],
    competencesWithoutDisciplines: [],
    lastChecked: null,
    validationInProgress: false
  })

  const editingScheme = ref(null)
  const schemeLoading = ref(false)
  const disciplineSchemes = ref([])

  const competenceIndicatorsData = ref([])
  const competenceIndicatorsCreteria = ref([])
  const indicatorsLoading = ref(false)


  // Вспомогательные функции
  const _getGroupListParams = () => {
    return {
      year: selectedYear.value,
      text: textFilter.value,
      groupText: groupTextFilter.value,
      status: statusFilter.value,
      my: myFilter.value
    }
  }

  const _handleApiError = (error, operation) => {
    console.error(`Error ${operation}:`, error)
    throw error
  }

  const _setLoadingState = (isLoading, target = null) => {
    if (target) {
      target.value = isLoading
    } else {
      loading.value = isLoading
    }
  }

  const _fetchWithPlanId = async (endpoint, planId, params = {}, loadingTarget = null) => {
    if (!planId) {
      throw new Error('Plan ID is required')
    }
    
    _setLoadingState(true, loadingTarget)
    try {
      const response = await api.get(endpoint, { params: { plan_id: planId, ...params } })
      return response.data
    } catch (error) {
      _handleApiError(error, `fetching from ${endpoint}`)
    } finally {
      _setLoadingState(false, loadingTarget)
    }
  }

  const _resetData = (dataRef, defaultValue = []) => {
    dataRef.value = defaultValue
  }

  const _updateMatrixValidation = (isValid, disciplinesWithoutCompetences = [], competencesWithoutDisciplines = []) => {
    matrixValidation.value = {
      isValid,
      disciplinesWithoutCompetences,
      competencesWithoutDisciplines,
      lastChecked: new Date(),
      validationInProgress: false
    }

    if (currentPlanId.value) {
      localStorage.setItem(`matrix_valid_${currentPlanId.value}`, isValid ? 'true' : 'false')
      
      if (isValid) {
        localStorage.setItem(`matrix_validation_${currentPlanId.value}`, JSON.stringify({
          isValid,
          checkedAt: new Date().toISOString()
        }))
      }
    }
  }

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
  function setCurrentPlanId(planId) {
    currentPlanId.value = planId;
    if (planId) {
      LocalStorage.set('current_plan_id', planId);
    } else {
      LocalStorage.remove('current_plan_id');
    }
  }


  async function fetchGroupsList() {
    _setLoadingState(true)
    try {
      const response = await api.get('/api/competence/group-list/', { 
        params: _getGroupListParams() 
      })
      groupsList.value = response.data
    } catch (error) {
      _handleApiError(error, 'fetching groups list')
      _resetData(groupsList)
    } finally {
      _setLoadingState(false)
    }
  }

  async function fetchGroupPrograms(planId) {
    _setLoadingState(true)
    try {
      setCurrentPlanId(planId);
      const response = await api.get(`/api/competence/${planId}/group-program/`)
      currentGroupPrograms.value = response.data
    } catch (error) {
      _handleApiError(error, 'fetching group programs')
      _resetData(currentGroupPrograms)
    } finally {
      _setLoadingState(false)
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
      _handleApiError(error, 'fetching program detail')
    }
  }

  async function fetchAllCompetences(planId) {
    try {
      const data = await _fetchWithPlanId('/api/competence/all-competences/', planId)
      currentPlanCompetences.value = data.competences
      return data
    } catch (error) {
      _resetData(currentPlanCompetences)
    }
  }

  async function fetchAllDisciplines(planId) {
    try {
      const data = await _fetchWithPlanId('/api/competence/all-disciplines/', planId)
      currentPlanDisciplines.value = data.disciplines
      return data
    } catch (error) {
      _resetData(currentPlanDisciplines)
    }
  }

  async function fetchCompetenceMatrix(planId) {
    try {
      const data = await _fetchWithPlanId(
        '/api/competence/competence-matrix/', 
        planId, 
        {}, 
        matrixLoading
      )
      competenceMatrix.value = data.matrix || []
      return data
    } catch (error) {
      _resetData(competenceMatrix)
    }
  }

  async function fetchDisciplineCompetencesDetailed(planId, disciplineId) {
    _setLoadingState(true)
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
      _handleApiError(error, 'fetching detailed discipline competences')
    } finally {
      _setLoadingState(false)
    }
  }
  
  async function updateDisciplineCompetences(selectedCompetences) {
    _setLoadingState(true, saving)
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
      _handleApiError(error, 'updating discipline competences')
    } finally {
      _setLoadingState(false, saving)
    }
  }
  
  function clearEditingDiscipline() {
    editingDiscipline.value = null
    disciplineCompetences.value = []
  }

  // Валидация матрицы
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
      
      _updateMatrixValidation(isValid, disciplinesWithoutCompetences, competencesWithoutDisciplines)
      
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

  async function fetchCompetenceSchema(planId) {
    try {
      const data = await _fetchWithPlanId(
        '/api/competence/competence-schema-data/', 
        planId, 
        {}, 
        schemaLoading
      )
      schemaData.value = data.schema_rows || []
      return data
    } catch (error) {
      _resetData(schemaData)
    }
  }

  async function fetchDisciplineSchemes(planId, disciplineId) {
    _setLoadingState(true, schemeLoading)
    try {
      if (!planId || !disciplineId) {
        throw new Error('Plan ID and Discipline ID are required')
      }
      
      const response = await api.get('/api/competence/discipline-semester-schemes/', {
        params: { 
          plan_id: planId,
          discipline_id: disciplineId
        }
      })
      
      disciplineSchemes.value = response.data.competence_schemes || []
      
      return response.data
    } catch (error) {
      _handleApiError(error, 'fetching discipline schemes')
      _resetData(disciplineSchemes)
    } finally {
      _setLoadingState(false, schemeLoading)
    }
  }

  async function updateSemesterScheme(payload) {
    _setLoadingState(true, saving)
    try {
      const response = await api.post(
        '/api/competence/update-semester-scheme/', 
        payload
      )

      if (editingDiscipline.value) {
        await fetchDisciplineSchemes(
          editingDiscipline.value.planId,
          editingDiscipline.value.id
        )
      }
      
      if (currentPlanId.value) {
        await fetchCompetenceSchema(currentPlanId.value)
      }
      
      return response.data
    } catch (error) {
      _handleApiError(error, 'updating semester scheme')
    } finally {
      _setLoadingState(false, saving)
    }
  }

  function setEditingScheme(data) {
    editingScheme.value = data
  }

  function clearEditingScheme() {
    editingScheme.value = null
  }

  async function fetchPlanDetails(planId) {
    _setLoadingState(true)
    try {
      if (!planId) {
        throw new Error('Plan ID is required')
      }
      
      const response = await api.get('/api/competence/plan-details/', { 
        params: { plan_id: planId } 
      })
      return response.data
    } catch (error) {
      console.error('Error fetching plan details:', error)
      return null
    } finally {
      _setLoadingState(false)
    }
  }

  async function fetchCompetenceRelations(planId, competenceIndex) {
    _setLoadingState(true)
    try {
      if (!planId || !competenceIndex) {
        throw new Error('Plan ID и индекс компетенции обязательны')
      }
      
      const response = await api.get('/api/competence/competence-relations/', {
        params: { 
          plan_id: planId,
          competence_index: competenceIndex
        }
      })
      
      return response.data
    } catch (error) {
      console.error('Error fetching competence relations:', error)
      throw error
    } finally {
      _setLoadingState(false)
    }
  }

  async function updateCompetenceRelations(planId, competenceIndex, relationsText) {
    _setLoadingState(true, saving)
    try {
      if (!planId || !competenceIndex) {
        throw new Error('Plan ID и индекс компетенции обязательны')
      }
      
      const payload = {
        plan_id: planId,
        competence_index: competenceIndex,
        relations_text: relationsText || ''
      }
      
      const response = await api.post('/api/competence/update-competence-relations/', payload)
      
      return response.data
    } catch (error) {
      console.error('Error updating competence relations:', error)
      throw error
    } finally {
      _setLoadingState(false, saving)
    }
  }

  async function fetchCompetenceFinalIndicators(planId, competenceIndex) {
    _setLoadingState(true)
    try {
      if (!planId || !competenceIndex) {
        throw new Error('Plan ID и индекс компетенции обязательны')
      }
      
      const response = await api.get('/api/competence/competence-final-indicators/', {
        params: { 
          plan_id: planId,
          competence_index: competenceIndex
        }
      })
      
      return response.data
    } catch (error) {
      console.error('Error fetching competence final indicators:', error)
      throw error
    } finally {
      _setLoadingState(false)
    }
  }

  async function updateCompetenceFinalIndicators(planId, competenceIndex, finalIndicatorText, indicatorId = null) {
    _setLoadingState(true, saving)
    try {
      if (!planId || !competenceIndex) {
        throw new Error('Plan ID и индекс компетенции обязательны')
      }
      
      const payload = {
        plan_id: planId,
        competence_index: competenceIndex,
        final_indicator_text: finalIndicatorText || ''
      }
      
      if (indicatorId) {
        payload.indicator_id = indicatorId
      }
      
      const response = await api.post('/api/competence/update-competence-final-indicators/', payload)
      
      return response.data
    } catch (error) {
      console.error('Error updating competence final indicators:', error)
      throw error
    } finally {
      _setLoadingState(false, saving)
    }
  }

  async function fetchCompetenceIndicatorDisciplines(planId, competenceIndex) {
    _setLoadingState(true)
    try {
      if (!planId || !competenceIndex) {
        throw new Error('Plan ID и индекс компетенции обязательны')
      }
      
      const response = await api.get('/api/competence/competence-indicator-disciplines/', {
        params: { 
          plan_id: planId,
          competence_index: competenceIndex
        }
      })
      
      return response.data
    } catch (error) {
      console.error('Error fetching competence indicator disciplines:', error)
      throw error
    } finally {
      _setLoadingState(false)
    }
  }

  async function updateIndicatorContent(indicatorId, newContent) {
    _setLoadingState(true, saving)
    try {
      if (!indicatorId || typeof newContent !== 'string') {
        throw new Error('ID индикатора и новое содержание обязательны')
      }
      
      const payload = {
        indicator_id: indicatorId,
        indicator_content: newContent || ''
      }
      
      const response = await api.post('/api/competence/update-indicator-content/', payload)
      
      return response.data
    } catch (error) {
      console.error('Error updating indicator content:', error)
      throw error
    } finally {
      _setLoadingState(false, saving)
    }
  }

  async function fetchCompetenceIndicators(planId, competenceIndex) {
    _setLoadingState(true, indicatorsLoading)
    try {
      if (!planId || !competenceIndex) {
        throw new Error('Plan ID и индекс компетенции обязательны')
      }
      
      const response = await api.get('/api/competence/competence-indicator-disciplines/', {
        params: { 
          plan_id: planId,
          competence_index: competenceIndex
        }
      })
      const tableData = response.data.table_data || []
      const indicatorsWithDetails = await Promise.all(
        tableData.map(async (indicator) => {
          try {
            const detailsResponse = await api.get('/api/competence/indicator-details/', {
              params: {
                indicator_id: indicator.id
              }
            })

            return {
              ...indicator, 
              ...detailsResponse.data, 
              saving: false, 
              saved: false 
            }
          } catch (error) {
            console.warn(`Error loading details for indicator ${indicator.id}:`, error)
            return {
              ...indicator,
              know: '',
              able: '',
              own: '',
              criteria: '',
              methods: '',
              saving: false,
              saved: false
            }
          }
        })
      )
      
      competenceIndicatorsData.value = indicatorsWithDetails
      competenceIndicatorsCreteria.value = indicatorsWithDetails
      return response.data
    } catch (error) {
      console.error('Error fetching competence indicators:', error)
      _resetData(competenceIndicatorsData)
      _resetData(competenceIndicatorsCreteria)
      throw error
    } finally {
      _setLoadingState(false, indicatorsLoading)
    }
  }

  async function saveIndicatorDetails(indicatorData) {
    _setLoadingState(true, saving)
    try {
      const payload = {
        indicator_id: indicatorData.id,
        know: indicatorData.know || '',
        able: indicatorData.able || '',
        own: indicatorData.own || '',
        criteria: indicatorData.criteria || '',
        methods: indicatorData.methods || ''
      }
      
      const response = await api.post('/api/competence/save-indicator-details/', payload)

      const index = competenceIndicatorsData.value.findIndex(item => item.id === indicatorData.id)
      if (index !== -1) {
        competenceIndicatorsData.value[index] = {
          ...competenceIndicatorsData.value[index],
          ...response.data.indicator,
          saving: false,
          saved: true
        }
        competenceIndicatorsCreteria.value[index] = {
          ...competenceIndicatorsCreteria.value[index],
          ...response.data.indicator,
          saving: false,
          saved: true
        }
      }
      
      return response.data
    } catch (error) {
      console.error('Error saving indicator details:', error)
      throw error
    } finally {
      _setLoadingState(false, saving)
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

    setCurrentPlanId,
    
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
    getValidationStatus,

    schemaData,
    schemaLoading,
    fetchCompetenceSchema,
    editingScheme,

    schemeLoading,
    disciplineSchemes,
    fetchDisciplineSchemes,
    updateSemesterScheme,
    setEditingScheme,
    clearEditingScheme,

    fetchPlanDetails,

    fetchCompetenceRelations,
    updateCompetenceRelations,

    fetchCompetenceFinalIndicators,
    updateCompetenceFinalIndicators,

    fetchCompetenceIndicatorDisciplines,
    updateIndicatorContent,

    competenceIndicatorsData,
    competenceIndicatorsCreteria,
    indicatorsLoading,
    fetchCompetenceIndicators,
    saveIndicatorDetails,
  }
})