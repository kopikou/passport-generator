<script setup lang="ts">
import { ref, computed, watch, onBeforeMount, nextTick, defineAsyncComponent } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCompetencePassportStore } from 'src/stores/competencePassportStore'
import { storeToRefs } from 'pinia'
import { useQuasar, date } from 'quasar'

// Компоненты разделов
const TitlePageSection = defineAsyncComponent(() => import('./components/menu_sections/TitlePageSection.vue'))
const CompetenceRelationsSection = defineAsyncComponent(() => import('./components/menu_sections/CompetenceRelationsSection.vue'))
const CompetenceIndicatorsSection = defineAsyncComponent(() => import('./components/menu_sections/CompetenceIndicatorsSection.vue'))
const IndicatorDisciplinesSection = defineAsyncComponent(() => import('./components/menu_sections/IndicatorDisciplinesSection.vue'))
const IndicatorResultsSection = defineAsyncComponent(() => import('./components/menu_sections/IndicatorResultsSection.vue'))
const AssessmentCriteriaSection = defineAsyncComponent(() => import('./components/menu_sections/AssessmentCriteriaSection.vue'))

const route = useRoute()
const router = useRouter()
const $q = useQuasar()
const store = useCompetencePassportStore()

const {
  currentPlanId,
  planData,
  admissionInfo,
  passport,
  loading,
  currentCompetenceValidation,
  schemaValidation,
  validatingSchema,
  schemaValidationStatus,
  schemaValidationColumns,
  lastSchemaCheckedFormatted,
} = storeToRefs(store)

const currentCompetence = ref<any>(null)

const exporting = ref(false)

const showValidationErrors = ref(false)

function navigateToFix(errorRow) {
  // Перенаправляем на страницу схемы 
  router.push({
    name: 'competenceSchema',
    params: { id: currentPlanId.value },
    query: {
      discipline_id: errorRow.discipline_id,
      competence_index: errorRow.competence_index,
      semester: errorRow.semester
    }
  })
}

async function navigateToPassportFix(errorRow) {
  try {
    const result = await store.fixSchemeIndicators(
      errorRow.discipline_id,
      errorRow.competence_index,
      errorRow.scheme_forms_count,
      errorRow.indicators_count
    )
    
    if (result.success) {
      $q.notify({ type: 'positive', position: 'top-right', message: result.message, timeout: 5000 })
    }
  } catch (error) {
    $q.notify({ type: 'warning', position: 'top-right', message: 'Не удалось автоматически скорректировать индикаторы' })
  }
  await store.validateSchemeIndicators()
  await loadPlanData()
  // Перенаправляем на паспорт с нужной компетенцией и разделом 2.1
  router.push({
    name: 'competencePassport',
    params: { id: currentPlanId.value },
    query: {
      section: 'indicator-disciplines',
      competence: errorRow.competence_index
    }
  })
}

async function exportPassport() {
  exporting.value = true
  try {
    store.getPassportReport()    
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: 'Ошибка при генерации документа',
      position: 'top-right'
    })
  } finally {
    exporting.value = false
  }
}

const activeTab = ref('competence-relations')
const sectionComponents = {
  'title-page': TitlePageSection,
  'competence-relations': CompetenceRelationsSection,
  'competence-indicators': CompetenceIndicatorsSection,
  'indicator-disciplines': IndicatorDisciplinesSection,
  'indicator-results': IndicatorResultsSection,
  'assessment-criteria': AssessmentCriteriaSection
}

const selectedSection = computed(() => {
  return (route.query.section as string) || ''
})

const currentCompetenceIndex = computed(() => {
  return (route.query.competence as string) || ''
})

const currentSectionComponent = computed(() => {
  if (!selectedSection.value) return null
  return sectionComponents[selectedSection.value as keyof typeof sectionComponents] || null
})

function onTabChange(tabName) {
  if (!currentCompetenceIndex.value || !currentPlanId.value || tabName === selectedSection.value) {
    return
  }
  router.push({
    name: 'competencePassport',
    params: { id: route.params.id },
    query: { 
      section: tabName,
      competence: currentCompetenceIndex.value
    }
  })
}

async function loadPlanData() {
  try {
    //await store.fetchPlanAdmissionData(currentPlanId.value)
    await store.fetchPassport(currentPlanId.value)
  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: `Ошибка загрузки данных плана: ${error.message}`,
      position: 'top-right'
    })
  }
}

async function loadCompetenceData(competenceIndex) {
  if (!competenceIndex || !currentPlanId.value) {
    currentCompetence.value = null
    return
  }
  
  try {
    const competence = passport.value.find(comp => comp.competence_index === competenceIndex)
    if (competence) {
      currentCompetence.value = competence
    } else {
      currentCompetence.value = null
      // $q.notify({
      //   type: 'warning',
      //   message: `Компетенция ${competenceIndex} не найдена в паспорте`,
      //   position: 'top-right'
      // })
    }
  } catch (error: any) {
    $q.notify({
      type: 'negative',
      message: `Ошибка загрузки данных компетенции: ${error.message}`,
      position: 'top-right'
    })
    currentCompetence.value = null
  }
}

const updateActiveTab = () => {
  if (selectedSection.value && selectedSection.value !== 'title-page') {
    activeTab.value = selectedSection.value
  }
}

const currentCompetenceValidationStatus = computed(() => {
  return currentCompetenceValidation.value(currentCompetence.value)
})

onBeforeMount(async () => {
  await loadPlanData()
  await store.validateSchemeIndicators()

  if (route.query.competence) {
    await loadCompetenceData(route.query.competence as string)
  }
  
  await nextTick()
  updateActiveTab()
})

watch(
  () => route.query,
  async (newQuery) => {
    if (newQuery.section === 'title-page') {
      currentCompetence.value = null
    } else if (newQuery.competence) {
      await loadCompetenceData(newQuery.competence as string)
    } else {
      currentCompetence.value = null
    }
    await nextTick()
    updateActiveTab()
  },
  { immediate: true, deep: true }
)

watch(currentPlanId.value, async (newPlanId) => {
    if (newPlanId) {
      //await loadPlanData()
      
      if (route.query.section === 'title-page') {

      } else if (route.query.competence) {
        await loadCompetenceData(route.query.competence as string)
      }
    } else {
      currentCompetence.value = null
    }
    await nextTick()
    updateActiveTab()
  }
)
</script>

<template>
  <div class="competence-passport-view q-pa-sm">
    <!-- Блок валидации -->
    <div v-if="schemaValidationStatus" class="q-mb-md validation-container">
      <q-banner 
        :class="schemaValidationStatus.type === 'error' ? 'bg-negative text-white' : 'bg-positive text-white'"
        rounded
      >
        <template v-slot:avatar>
          <q-icon :name="schemaValidationStatus.type === 'error' ? 'warning' : 'check_circle'" size="24px" />
        </template>
        
        <div class="text-body1 q-mb-xs">{{ schemaValidationStatus.title }}</div>
        <div class="text-body2">{{ schemaValidationStatus.message }}</div>
        
        <template v-if="schemaValidationStatus.details" v-slot:action>
          <q-btn 
            flat 
            :color="schemaValidationStatus.type === 'error' ? 'white' : 'dark'" 
            :label="showValidationErrors ? 'Скрыть детали' : 'Показать детали'" 
            @click="showValidationErrors = !showValidationErrors"
            class="q-mr-sm"
          />
          <q-btn 
            v-if="schemaValidationStatus.type === 'error'"
            flat 
            :color="schemaValidationStatus.type === 'error' ? 'white' : 'dark'" 
            label="Обновить проверку" 
            @click="runSchemaValidation()"
            :loading="validatingSchema"
            icon="refresh"
          />
        </template>
      </q-banner>
      
      <q-slide-transition>
        <div v-if="showValidationErrors && schemaValidation?.errors?.length" class="validation-details q-pa-md bg-grey-2 q-mt-sm">
          <q-card class="q-mb-md">
            <q-card-section class="q-pa-none">
              <q-table
                :rows="schemaValidation.errors"
                :columns="schemaValidationColumns"
                row-key="id"
                dense
                flat
                bordered
              >
                <template v-slot:body-cell-actions="props">
                  <q-td :props="props">
                    <div class="column items-center q-gutter-y-xs">
                      <q-btn
                        size="sm"
                        color="primary"
                        label="Исправить в схеме"
                        @click="navigateToFix(props.row)"
                        title="Изменить формы аттестации"
                        :loading="validatingSchema"
                      />
                      <q-btn
                        size="sm"
                        color="primary"
                        label="Исправить в паспорте"
                        @click="navigateToPassportFix(props.row)"
                        title="Изменить число индикаторов"
                        :loading="store.saving"
                      />
                    </div>
                  </q-td>
                </template>
              </q-table>
            </q-card-section>
          </q-card>

          <div class="text-caption">
            <q-icon name="info" class="q-mr-xs" />
            Проверка выполнена: {{ lastSchemaCheckedFormatted }}
          </div>
        </div>
      </q-slide-transition>
    </div>

    <div class="section-header q-mb-md">
      <div class="row justify-content-between">
        <div class="col text-h4 q-mb-xs">Паспорт компетенций</div>
          <div class="col-auto">
          <q-btn
            flat
            dense
            icon="file_download"
            label="Выгрузить"
            @click="exportPassport"
            :loading="exporting"
            class="q-mr-sm q-pr-sm bg-primary text-white"
            
          >
            <q-tooltip>Скачать паспорт компетенций в формате Word</q-tooltip>
          </q-btn>
          </div>
      </div>
      <div v-if="currentCompetence" class="text-subtitle1 text-grey">
        {{ currentCompetence.competence_index }} - {{ currentCompetence.competence }}
      </div>
      <div v-else-if="selectedSection === 'title-page'" class="text-subtitle1 text-grey">
        Титульный лист паспорта компетенций
      </div>
    </div>
    
    <div v-if="!selectedSection" class="empty-state q-pa-xl text-center">
      <span style="align-content: center; text-align: center; font-size: 20px; font-weight: bold">
        Выберите нужный раздел слева
      </span>
    </div>
    
    <div v-else class="passport-content">
      <!-- Вкладки для разделов компетенции -->
      <div v-if="selectedSection && selectedSection !== 'title-page'" class="competence-tabs q-mb-lg">
        <q-tabs
          v-model="activeTab"
          align="left"
          class="q-mb-md"
          active-bg-color="teal-1"
          @update:model-value="onTabChange"
        >
          <q-tab
            class="text-teal"
            name="competence-relations"
            label="1.1. Связь с компетенциями"
          >
            <q-icon
              v-if="currentCompetenceValidationStatus['competence-relations']" 
              name="error"
              color="red"
              size="12px"
              class="validation-icon"
            />
          </q-tab>
          <q-tab
            class="text-teal"
            name="competence-indicators"
            label="2. Индикаторы достижения"
          >
            <q-icon
              v-if="currentCompetenceValidationStatus['final-indicator']" 
              name="error"
              color="red"
              size="12px"
              class="validation-icon"
            />
          </q-tab>
          <q-tab
            class="text-teal"
            name="indicator-disciplines"
            label="2.1. Индикаторы и дисциплины"
          >
            <q-icon
              v-if="currentCompetenceValidationStatus['competence-indicators']" 
              name="error"
              color="red"
              size="12px"
              class="validation-icon"
            />
          </q-tab>
          <q-tab
            class="text-teal"
            name="indicator-results"
            label="2.2. Результаты обучения"
          >
            <q-icon
              v-if="currentCompetenceValidationStatus['indicator-results']" 
              name="error"
              color="red"
              size="12px"
              class="validation-icon"
            />
          </q-tab>
          <q-tab
            class="text-teal"
            name="assessment-criteria"
            label="3. Критерии оценивания"
          >
            <q-icon
              v-if="currentCompetenceValidationStatus['assessment-criteria']" 
              name="error"
              color="red"
              size="12px"
              class="validation-icon"
            />
          </q-tab>
        </q-tabs>
      </div>
      
      <!-- Динамический контент по разделам -->
      <div v-if="loading" class="text-center q-pa-lg">
        <q-spinner color="primary" size="2em" />
        <div class="text-caption q-mt-sm">Загрузка данных...</div>
      </div>
      
      <div v-else class="section-content">
        <component
          v-if="currentSectionComponent"
          :is="currentSectionComponent"
          :plan-data="planData"
          :admission-info="admissionInfo"
          :competence="currentCompetence"
          :plan-id="planData.id"
        />
        <div v-else class="text-center q-pa-xl text-grey">
          <q-icon name="error_outline" size="xl" class="q-mb-md" />
          <div class="text-h6">Раздел не найден</div>
          <div class="text-body2 q-mt-sm">Пожалуйста, выберите другой раздел</div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.validation-container {
  .q-banner {
    border-left: 4px solid;
    
    &.bg-negative {
      border-left-color: darken(#f44336, 10%);
    }
    
    &.bg-positive {
      border-left-color: darken(#4CAF50, 10%);
    }
  }

  .validation-details {
    border-radius: 0 0 8px 8px;
    border: 1px solid rgba(0,0,0,0.1);
    border-top: none;
    overflow-x: auto;
    width: 100%;
    max-width: 100%;  
    
    :deep(.q-table) {
      width: 100%;
      table-layout: fixed;
      overflow-y: auto;
      th {
        vertical-align: middle !important;
        white-space: nowrap !important;   
        overflow: hidden;
      }
      
      td, th {
        word-break: break-word;  
        white-space: normal;  

        &:nth-child(1) {
          width: 130px;
          min-width: 100px;
          max-width: 150px;
        }

        &:nth-child(2) {
          width: 250px;
          min-width: 200px;
          max-width: 350px;
        }
        
        &:nth-child(3) {
          width: 70px;
          min-width: 70px;
          max-width: 70px;
        }

        &:nth-child(4) {
          width: 300px;
          min-width: 200px;
          max-width: 400px;
        }
      }
    }
  }
}

.competence-passport-view {
  min-height: 100%;
  
  .section-header {
    border-bottom: 1px solid #e0e0e0;
    padding-bottom: 16px;
    
    .text-subtitle1 {
      font-size: 16px;
      line-height: 1.4;
    }
  }
  
  .competence-tabs {
    .q-tabs {
      .q-tab {
        text-transform: none;
        position: relative;
      }
    }
  }
  
  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 400px;
    
    span {
      font-size: 20px;
      font-weight: bold;
      line-height: 1.5;
    }
  }
  
  .passport-content {
    min-height: 300px;
  }
  
  .section-content {
    max-width: 1200px;
    margin: 0 auto;
  }
}

.validation-icon {
    position: absolute;
    top: 2px;
    right: -8px;
    z-index: 1;
  }
</style>