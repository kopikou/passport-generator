<template>
  <layout-h-c-f>
    <template #header>
      <div class="q-px-sm q-pb-sm">
        <div class="flex justify-between q-my-sm q-px-sm"
             style="display: grid; grid-template-columns: 1fr 220px auto auto; gap: 8px; align-items: center;">
          <q-input 
            outlined 
            label="Поиск по направлению, аббревиатуре, специальности, коду и т.д." 
            v-model="groupTextFilter" 
            clearable
            @update:model-value="handleSearchChange"
          />
          <q-select
            v-model="selectedYear"
            label="Год"
            :options="yearsList"
            @update:model-value="handleYearChange"
          />
        </div>
      </div>
    </template>
    <template #content>
      <div v-if="groupsList.length > 0"
           style="display: grid; grid-template-columns: 300px 1fr; overflow: hidden; height: 100%"
      >
        <!-- Левая панель со списком групп -->
        <q-list
          style="overflow-y: auto; height: 100%; box-shadow: 0 0 8px silver; z-index: 100"
          separator
        >
          <q-item
            v-for="group in filteredGroups"
            :key="group.plan_id"
            style="display: grid; gap: 8px;"
            clickable
            :active="currentPlanId === group.plan_id"
            @click="selectGroup(group.plan_id)"
            active-class="my-active-item"
          >
            <div style="display: grid; grid-template-columns: 1fr auto">
              <div style="display: flex; justify-content: left; font-size: 1.25rem;">
                {{ `${group.abbr}-${group.yr.toString().slice(-2)}` }}
              </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr auto">
              <a :href="getFirstPlxFile(group.plx_file)" v-if="getFirstPlxFile(group.plx_file)">*.plx</a>
            </div>
          </q-item>
        </q-list>

        <!-- Правая панель с выбором действия -->
        <div v-if="currentPlanId" style="display: flex; flex-direction: column; height: 100%; padding: 20px;">
          <div class="text-h5 q-mb-md">Выберите действие для группы</div>
          
          <!-- Карточки выбора действия -->
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
            <!-- Загрузка нового учебного плана -->
            <q-card class="cursor-pointer" @click="selectAction('upload')" :class="{ 'selected-card': selectedAction === 'upload' }">
              <q-card-section>
                <div class="text-h6">Загрузить учебный план</div>
                <div class="text-caption text-grey">
                  Загрузите новый файл учебного плана в формате .plx
                </div>
              </q-card-section>
              <q-card-actions>
                <q-btn color="primary" label="Загрузить" @click.stop="uploadPlan" />
              </q-card-actions>
            </q-card>

            <!-- Выбор существующего учебного плана -->
            <q-card class="cursor-pointer" @click="selectAction('select')" :class="{ 'selected-card': selectedAction === 'select' }">
              <q-card-section>
                <div class="text-h6">Выбрать существующий</div>
                <div class="text-caption text-grey">
                  Выберите прошлогодний учебный план
                </div>
              </q-card-section>
              <q-card-actions>
                <q-btn color="primary" label="Выбрать" @click.stop="selectExistingPlan" />
              </q-card-actions>
            </q-card>
          </div>

          <div v-if="selectedAction">
            <q-separator class="q-my-lg" />
            
            <!-- Загрузка плана -->
            <div v-if="selectedAction === 'upload'">
              <div class="text-h6 q-mb-md">Загрузка учебного плана</div>
              <q-file
                v-model="uploadedFile"
                label="Выберите файл учебного плана (.plx)"
                accept=".plx"
                outlined
                class="q-mb-md"
              />
              <q-btn 
                color="primary" 
                label="Загрузить файл" 
                :disable="!uploadedFile"
                @click="uploadPlanFile"
              />
            </div>

            <!-- Выбор существующего плана -->
            <div v-if="selectedAction === 'select'">
              <div class="text-h6 q-mb-md">Доступные учебные планы:</div>
              
              <!-- Список доступных файлов -->
              <div v-if="availablePlanFiles.length > 0">
                <q-list bordered>
                  <q-item 
                    v-for="(file, index) in availablePlanFiles" 
                    :key="index"
                    clickable
                    @click="selectPlanFile(file)"
                    :class="{ 'bg-blue-1': selectedPlanFile === file }"
                  >
                    <q-item-section>
                      <q-item-label>{{ file.name }}</q-item-label>
                      <q-item-label caption>{{ file.date }}</q-item-label>
                    </q-item-section>
                    <q-item-section side>
                      <q-btn 
                        icon="file_download" 
                        color="primary" 
                        flat 
                        dense
                        :href="file.url"
                        download
                        @click.stop
                      />
                    </q-item-section>
                  </q-item>
                </q-list>
                
                <q-btn 
                  color="primary" 
                  label="Выбрать план" 
                  class="q-mt-md"
                  :disable="!selectedPlanFile"
                  @click="confirmPlanSelection"
                />
              </div>

              <div v-else class="text-grey text-center q-pa-lg">
                Нет доступных учебных планов
              </div>
            </div>
          </div>
        </div>

        <span
          v-else
          style="align-content: center; text-align: center; font-size: 20px; font-weight: bold"
        >
          Выберите нужный раздел слева
        </span>
      </div>

    </template>
  </layout-h-c-f>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useCompetencePassportStore } from 'stores/competencePassportStore';
import { useRouter } from 'vue-router';
import { storeToRefs } from 'pinia'
import { LocalStorage, useQuasar } from 'quasar';
import _ from 'lodash';
import LayoutHCF from 'components/LayoutHCF.vue';
import dayjs from "dayjs";

const store = useCompetencePassportStore()
const {
  groupsList,
  currentPlanId,
  groupTextFilter,
  textFilter,
  statusFilter,
  myFilter,
  selectedYear
} = storeToRefs(store)
const router = useRouter()
const $q = useQuasar()

const selectedAction = ref('')
const uploadedFile = ref(null)
const selectedPlanFile = ref(null)

const yearsList = computed(() => {
  let year = 2025;
  let list = []
  while (year <= dayjs().year() + 1) {
    list.push(year);
    year += 1;
  }
  return list;
});

const filteredGroups = computed(() => {
  if (!groupTextFilter.value || groupTextFilter.value.trim() === '') {
    return groupsList.value;
  }
  
  const searchLower = groupTextFilter.value.toLowerCase().trim();
  
  return groupsList.value.filter(group => {
    const fieldsToSearch = [
      group.abbr,
      group.yr?.toString(),
      group.dir, 
      group.sp,
      group.kod, 
      group.spec, 
      group.name, 
    ];
    
    const fullMatchFields = [
      `${group.abbr}-${group.yr?.toString()?.slice(-2)}`,
    ];
    
    for (const field of fieldsToSearch) {
      if (field && field.toString().toLowerCase().includes(searchLower)) {
        return true;
      }
    }
    
    for (const field of fullMatchFields) {
      if (field && field.toLowerCase().includes(searchLower)) {
        return true;
      }
    }
    
    if (group.dir && typeof group.dir === 'object') {
      if (group.dir.name && group.dir.name.toLowerCase().includes(searchLower)) {
        return true;
      }
      if (group.dir.code && group.dir.code.toLowerCase().includes(searchLower)) {
        return true;
      }
    }
    
    return false;
  });
});

function getFirstPlxFile(plxFile) {
  if (!plxFile) return null;
  if (Array.isArray(plxFile) && plxFile.length > 0) {
    return plxFile[0];
  }
  return plxFile;
}

// Текущий файл учебного плана для выбранной группы
const currentGroupPlxFile = computed(() => {
  if (!currentPlanId.value) return null;
  const currentGroup = groupsList.value.find(group => group.plan_id === currentPlanId.value);
  return getFirstPlxFile(currentGroup?.plx_file);
});
const availablePlanFiles = computed(() => {
  if (!currentGroupPlxFile.value) return [];
  
  return [
    {
      name: getFileName(currentGroupPlxFile.value),
      url: currentGroupPlxFile.value,
      date: new Date().toLocaleDateString()
    }
  ];
});

function getFileName(url) {
  if (!url) return '';
  if (typeof url !== 'string') {
    console.warn('getFileName received non-string:', url);
    return 'Учебный план';
  }
  
  try {
    const fileName = url.split('/').pop() || 'Учебный план';
    return decodeURIComponent(fileName);
  } catch (error) {
    console.warn('Error decoding filename:', error);
    return url.split('/').pop() || 'Учебный план';
  }
}

function handleSearchChange() {
  if (groupTextFilter.value && groupTextFilter.value.trim() !== '') {
    LocalStorage.set('surp_rpdgroupfilter', groupTextFilter.value);
  } else {
    LocalStorage.remove('surp_rpdgroupfilter');
  }
  debouncedFetchGroupsList();
}

function handleYearChange() {
  debouncedFetchGroupsList();
}

const debouncedFetchGroupsList = _.debounce(async () => {
  await store.fetchGroupsList();
}, 300);

async function selectGroup(planId) {
  store.setCurrentPlanId(planId);
  selectedAction.value = '';
  selectedPlanFile.value = null;
  uploadedFile.value = null;

  await store.fetchAllDisciplines(planId);
}

function selectAction(action) {
  selectedAction.value = action;
}

function uploadPlan() {
  selectedAction.value = 'upload';
}

function selectExistingPlan() {
  selectedAction.value = 'select';
}

function selectPlanFile(file) {
  selectedPlanFile.value = file;
}

async function uploadPlanFile() {
  if (!uploadedFile.value) {
    $q.notify({
      type: 'warning',
      message: 'Выберите файл для загрузки'
    });
    return;
  }

  try {
    $q.notify({
      type: 'info',
      message: 'Функция загрузки будет реализована позже'
    });
    
    uploadedFile.value = null;
    
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: 'Ошибка при загрузке файла'
    });
  }
}

async function confirmPlanSelection() {
  if (!selectedPlanFile.value) {
    $q.notify({
      type: 'warning',
      message: 'Выберите учебный план'
    });
    return;
  }

  try {
    router.push(`/competence/reference`);
    $q.notify({
      type: 'positive',
      message: `Выбран учебный план: ${selectedPlanFile.value.name}`
    });
    
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: 'Ошибка при выборе учебного плана'
    });
  }
}

onMounted(async () => {
  const savedFilter = LocalStorage.getItem('surp_rpdgroupfilter');
  if (savedFilter !== null && savedFilter !== undefined && savedFilter !== 'null') {
    groupTextFilter.value = savedFilter;
  } else {
    groupTextFilter.value = '';
    LocalStorage.remove('surp_rpdgroupfilter');
  }
  
  await store.fetchGroupsList();
})

watch([
  () => textFilter.value,
  () => statusFilter.value,
  () => myFilter.value,
], _.debounce(async () => {
  await store.fetchGroupsList();
}, 300))
</script>

<style scoped lang="scss">
:deep(.table-header) {
  position: sticky;
  z-index: 1;
  top: 0;
  background: $blue-grey-2;
}

:deep(.my-active-item) {
  background: $blue-grey-2;
}

.selected-card {
  border: 2px solid $primary;
}
</style>