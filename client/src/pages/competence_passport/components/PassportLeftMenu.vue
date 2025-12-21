<template>
  <div class="competence-menu">
    <div class="menu-header q-pa-sm bg-grey-3">
      <div class="text-h6 text-weight-bold">Компетенции</div>
      <div class="text-caption text-grey q-mb-sm">
        Всего: {{ filteredCompetences.length }}
      </div>
      
      <!-- Поиск и фильтры -->
      <div class="q-gutter-y-sm">
        <q-input
          v-model="searchText"
          placeholder="Поиск по индексу..."
          dense
          outlined
          clearable
          class="bg-white"
          @update:model-value="handleSearch"
        >
          <template v-slot:prepend>
            <q-icon name="search" />
          </template>
        </q-input>
        
        <q-select
          v-model="selectedType"
          :options="competenceTypes"
          label="Фильтр по типу"
          dense
          outlined
          clearable
          emit-value
          map-options
          class="bg-white"
          @update:model-value="handleTypeFilter"
        />
      </div>
    </div>

    <div v-if="loading" class="q-pa-lg text-center">
      <q-spinner color="primary" size="2em" />
      <div class="text-caption q-mt-sm">Загрузка компетенций...</div>
    </div>

    <!-- Список компетенций -->
    <q-scroll-area v-else class="competence-scroll-area">
        
      <q-list class="competence-list" dense>
        <div v-if="filteredCompetences.length === 0" class="text-center q-py-lg text-grey">
          <q-icon name="info" size="md" class="q-mb-sm" />
          <div v-if="searchText || selectedType">Компетенции не найдены</div>
          <div v-else>Компетенции не загружены</div>
        </div>

        <!-- Титульный лист  -->
        <q-item 
          clickable
          v-ripple
          class="title-page-header q-mb-sm"
          @click="navigateToTitlePage"
          :active="isTitlePageActive()"
          active-class="active-menu-item"
        >
          <q-item-section>
            <q-item-label class="text-weight-medium">
              Титульный лист
            </q-item-label>
          </q-item-section>
        </q-item>

        <!-- Компетенции -->
        <template v-for="comp in filteredCompetences" :key="comp.competence_index">
          <q-item 
            clickable
            v-ripple
            class="competence-header"
            :class="getCompetenceClass(comp.competence_index)"
            @click="toggleCompetence(comp.competence_index)"
            :active="isCompetenceActive(comp)"
            active-class="active-menu-item"
          >
            <q-item-section avatar>
              <q-btn
                flat
                dense
                round
                size="sm"
                :icon="isCompetenceExpanded(comp.competence_index) ? 'keyboard_arrow_down' : 'keyboard_arrow_down'"
                :class="{ 'rotate-180': isCompetenceExpanded(comp.competence_index) }"
                class="transition-transform"
                style="min-width: 24px; min-height: 24px;"
              />
            </q-item-section>
            <q-item-section>
              <q-item-label class="text-weight-medium">
                {{ comp.competence_index }}
              </q-item-label>
            </q-item-section>
            <q-item-section side>
              <q-badge :color="getTypeBadgeColor(comp.competence_index)" rounded>
                {{ getCompetenceType(comp.competence_index) }}
              </q-badge>
            </q-item-section>
          </q-item>

          <!-- Подменю компетенции -->
          <q-slide-transition>
            <div v-if="isCompetenceExpanded(comp.competence_index)" class="competence-submenu">
              <!-- 1.1 Связь компетенции с иными компетенциями -->
              <q-item
                clickable
                v-ripple
                class="submenu-item"
                @click="navigateToCompetenceRelations(comp)"
                :active="isSectionActive(comp, 'competence-relations')"
                active-class="active-menu-item"
              >
                <q-item-section>
                  <div class="text-caption">1.1. Связь компетенции с иными компетенциях</div>
                </q-item-section>
              </q-item>

              <!-- 2. Индикаторы достижения компетенции -->
              <q-item
                clickable
                v-ripple
                class="submenu-item"
                @click="navigateToCompetenceIndicators(comp)"
                :active="isSectionActive(comp, 'competence-indicators')"
                active-class="active-menu-item"
              >
                <q-item-section>
                  <div class="text-caption">2. Индикаторы достижения компетенции</div>
                </q-item-section>
              </q-item>

              <!-- 2.1. Соотнесение индикаторов с дисциплинами -->
              <q-item
                clickable
                v-ripple
                class="submenu-item"
                @click="navigateToIndicatorDisciplines(comp)"
                :active="isSectionActive(comp, 'indicator-disciplines')"
                active-class="active-menu-item"
              >
                <q-item-section>
                  <div class="text-caption">2.1. Соотнесение индикаторов с дисциплинами</div>
                </q-item-section>
              </q-item>

              <!-- 2.2. Соотнесение индикаторов с результатами обучения -->
              <q-item
                clickable
                v-ripple
                class="submenu-item"
                @click="navigateToIndicatorResults(comp)"
                :active="isSectionActive(comp, 'indicator-results')"
                active-class="active-menu-item"
              >
                <q-item-section>
                  <div class="text-caption">2.2. Соотнесение индикаторов с результатами обучения</div>
                </q-item-section>
              </q-item>

              <!-- 3. Критерии и средства оценивания индикаторов -->
              <q-item
                clickable
                v-ripple
                class="submenu-item"
                @click="navigateToAssessmentCriteria(comp)"
                :active="isSectionActive(comp, 'assessment-criteria')"
                active-class="active-menu-item"
              >
                <q-item-section>
                  <div class="text-caption">3. Критерии и средства оценивания индикаторов</div>
                </q-item-section>
              </q-item>
            </div>
          </q-slide-transition>
        </template>
      </q-list>
    </q-scroll-area>

    <!-- Кнопки управления -->
    <div v-if="!loading && filteredCompetences.length > 0" class="q-pa-sm bg-grey-2 border-top">
      <q-btn
        flat
        dense
        color="primary"
        :icon="allExpanded ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
        :label="allExpanded ? 'Свернуть все' : 'Раскрыть все'"
        @click="toggleAll"
        class="full-width"
        size="sm"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useCompetencePassportStore } from 'stores/competencePassportStore'
import { storeToRefs } from 'pinia'
import { useQuasar } from 'quasar'

const router = useRouter()
const $route = useRoute()
const store = useCompetencePassportStore()
const {
  currentPlanId,
  currentPlanCompetences,
} = storeToRefs(store)

const $q = useQuasar()

const searchText = ref('')
const selectedType = ref('')
const expandedCompetences = ref(new Set())
const loading = ref(false)
const competencesData = ref([])

// Типы компетенций для фильтра
const competenceTypes = [
  { label: 'Универсальные (УК)', value: 'Универсальная' },
  { label: 'Общепрофессиональные (ОПК)', value: 'Общепрофессиональная' },
  { label: 'Профессиональные (ПК)', value: 'Профессиональная' },
  { label: 'Дополнительные (ДК)', value: 'Дополнительная' },
  { label: 'Другие', value: 'Другая' }
]

// Определяем тип компетенции по индексу
const getCompetenceType = (competenceIndex) => {
  if (!competenceIndex) return 'Неизвестно'
  
  if (competenceIndex.includes('УК') || competenceIndex.startsWith('УК')) {
    return 'Универсальная'
  }
  if (competenceIndex.includes('ОПК') || competenceIndex.startsWith('ОПК')) {
    return 'Общепрофессиональная'
  }
  if (competenceIndex.includes('ПК') || competenceIndex.startsWith('ПК')) {
    return 'Профессиональная'
  }
  if (competenceIndex.includes('ДК') || competenceIndex.startsWith('ДК')) {
    return 'Дополнительная'
  }
  
  return 'Другая'
}

const getTypeBadgeColor = (competenceIndex) => {
  const type = getCompetenceType(competenceIndex)
  const colors = {
    'Универсальная': 'blue',
    'Общепрофессиональная': 'green',
    'Профессиональная': 'orange',
    'Дополнительная': 'purple',
    'Другая': 'grey'
  }
  return colors[type] || 'grey'
}

const getCompetenceClass = (competenceIndex) => {
  const type = getCompetenceType(competenceIndex)
  return `competence-${type.toLowerCase().replace(/ /g, '-')}`
}

const isTitlePageActive = () => {
  return $route.query.section === 'title-page'
}

const isCompetenceActive = (competence) => {
  return $route.params.competenceId === competence.competence_index && 
         $route.query.section && 
         $route.query.section !== 'title-page'
}

const isSectionActive = (competence, sectionName) => {
  return $route.params.competenceId === competence.competence_index && 
         $route.query.section === sectionName
}

const filteredCompetences = computed(() => {
  let competences = competencesData.value
  
  if (searchText.value) {
    const searchLower = searchText.value.toLowerCase()
    competences = competences.filter(comp => 
      comp.competence_index.toLowerCase().includes(searchLower)
    )
  }
  
  if (selectedType.value) {
    competences = competences.filter(comp => 
      getCompetenceType(comp.competence_index) === selectedType.value
    )
  }
  
  return competences
})

const isCompetenceExpanded = (competenceIndex) => {
  if ($route.params.competenceId === competenceIndex) {
    return true
  }
  return expandedCompetences.value.has(competenceIndex)
}

const toggleCompetence = (competenceIndex) => {
  if (isCompetenceExpanded(competenceIndex)) {
    expandedCompetences.value.delete(competenceIndex)
  } else {
    expandedCompetences.value.add(competenceIndex)
  }
}

const allExpanded = computed(() => {
  return filteredCompetences.value.length > 0 && 
         filteredCompetences.value.every(comp => 
           isCompetenceExpanded(comp.competence_index)
         )
})

const toggleAll = () => {
  if (allExpanded.value) {
    expandedCompetences.value.clear()
  } else {
    filteredCompetences.value.forEach(comp => {
      expandedCompetences.value.add(comp.competence_index)
    })
  }
}

const handleSearch = () => {
  expandedCompetences.value.clear()
}

const handleTypeFilter = () => {
  expandedCompetences.value.clear()
}

watch(() => $route.params.competenceId, (newCompetenceId) => {
  if (newCompetenceId) {
    expandedCompetences.value.add(newCompetenceId)
  }
})

watch(() => $route.query.section, (newSection) => {
  if (newSection === 'title-page') {
    expandedCompetences.value.clear()
  }
})

const navigateToTitlePage = () => {
  router.push({
    name: 'competencePassport',
    params: { 
      planId: currentPlanId.value
    },
    query: { 
      section: 'title-page'
    }
  })
}

const navigateToCompetenceRelations = (competence) => {
  router.push({
    name: 'competencePassport',
    params: { 
      planId: currentPlanId.value,
    },
    query: { 
      section: 'competence-relations',
      competence: competence.competence_index 
    }
  })
}

const navigateToCompetenceIndicators = (competence) => {
  router.push({
    name: 'competencePassport',
    params: { 
      planId: currentPlanId.value,
    },
    query: { 
      section: 'competence-indicators',
      competence: competence.competence_index 
    }
  })
}

const navigateToIndicatorDisciplines = (competence) => {
  router.push({
    name: 'competencePassport',
    params: { 
      planId: currentPlanId.value, 
    },
    query: { 
      section: 'indicator-disciplines',
      competence: competence.competence_index 
    }
  })
}

const navigateToIndicatorResults = (competence) => {
  router.push({
    name: 'competencePassport',
    params: { 
      planId: currentPlanId.value,
    },
    query: { 
      section: 'indicator-results',
      competence: competence.competence_index 
    }
  })
}

const navigateToAssessmentCriteria = (competence) => {
  router.push({
    name: 'competencePassport',
    params: { 
      planId: currentPlanId.value,
    },
    query: { 
      section: 'assessment-criteria',
      competence: competence.competence_index 
    }
  })
}

const loadCompetences = async () => {
  if (!currentPlanId.value) {
    competencesData.value = []
    return
  }

  loading.value = true
  try {
    const data = await store.fetchAllCompetences(currentPlanId.value)
    if (data && data.competences) {
      competencesData.value = data.competences

      if ($route.params.competenceId) {
        expandedCompetences.value.add($route.params.competenceId)
      }
    } else {
      competencesData.value = []
    }
  } catch (error) {
    console.error('Error loading competences:', error)
    $q.notify({
      type: 'negative',
      message: 'Ошибка загрузки компетенций',
      position: 'top-right'
    })
    competencesData.value = []
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  if (currentPlanId.value) {
    await loadCompetences()
  }
})

watch(() => currentPlanId.value, async (newPlanId) => {
  if (newPlanId) {
    await loadCompetences()
  } else {
    competencesData.value = []
    expandedCompetences.value.clear()
  }
})

watch(() => currentPlanCompetences.value, (newCompetences) => {
  if (newCompetences && newCompetences.length > 0) {
    competencesData.value = newCompetences

    if ($route.params.competenceId) {
      expandedCompetences.value.add($route.params.competenceId)
    }
  }
}, { deep: true })
</script>

<style scoped lang="scss">
.competence-menu {
  height: 100%;
  display: flex;
  flex-direction: column;
  
  .menu-header {
    border-bottom: 1px solid #e0e0e0;
    flex-shrink: 0;
  }
  
  .competence-scroll-area {
    flex: 1;
  }
  
  .competence-list {
    .title-page-header {
      border-bottom: 1px solid rgba(0,0,0,0.05);
      min-height: 60px;
      background-color: rgba(151, 151, 151, 0.05);
      border-left: 3px solid #8a8a8a;
      
      &:hover {
        background-color: rgba(144, 144, 145, 0.1);
      }
      
      .q-item__section--avatar {
        min-width: 40px;
      }
    }
    
    .competence-header {
      border-bottom: 1px solid rgba(0,0,0,0.05);
      min-height: 60px;
      
      &:hover {
        background-color: rgba(0,0,0,0.02);
      }
      
      &.competence-универсальная {
        border-left: 3px solid #2196F3;
        background-color: rgba(33, 150, 243, 0.03);
      }
      
      &.competence-общепрофессиональная {
        border-left: 3px solid #4CAF50;
        background-color: rgba(76, 175, 80, 0.03);
      }
      
      &.competence-профессиональная {
        border-left: 3px solid #FF9800;
        background-color: rgba(255, 152, 0, 0.03);
      }
      
      &.competence-дополнительная {
        border-left: 3px solid #9C27B0;
        background-color: rgba(156, 39, 176, 0.03);
      }
      
      &.competence-другая {
        border-left: 3px solid #9E9E9E;
        background-color: rgba(158, 158, 158, 0.03);
      }
    }
    
    .competence-submenu {
      background: rgba(0,0,0,0.01);
      border-left: 3px solid rgba(0,0,0,0.1);
      margin-left: 32px;
      
      .submenu-item {
        min-height: 40px;
        padding-left: 16px;
        border-bottom: 1px solid rgba(0,0,0,0.05);
        
        &:hover {
          background-color: rgba(0,0,0,0.03);
        }
        
        &:last-child {
          border-bottom: none;
        }
        
        .text-caption {
          font-size: 12px;
          line-height: 1.2;
        }
      }
    }
  }
  
  .border-top {
    border-top: 1px solid #e0e0e0;
  }
}

.active-menu-item {
  background-color: #e3f2fd !important; 
  color: #1976d2 !important;

  &.title-page-header {
    border-left-color: #1976d2 !important;
  }
  
  &.competence-header {
    border-left-color: #1976d2 !important;
    background-color: rgba(25, 118, 210, 0.1) !important;
  }
  
  &.submenu-item {
    border-left-color: #1976d2 !important;
    background-color: rgba(25, 118, 210, 0.1) !important;
    
    .text-caption {
      color: #1976d2 !important;
    }
    
    .q-icon {
      color: #1976d2 !important;
    }
  }
}

.q-btn {
  &.transition-transform {
    transition: transform 0.3s ease;
  }
  
  &.rotate-180 {
    transform: rotate(180deg);
  }
}

.q-badge {
  font-size: 10px;
  padding: 2px 6px;
  font-weight: 500;
}

:deep(.q-scrollarea__content) {
  width: 100%;
}
</style>