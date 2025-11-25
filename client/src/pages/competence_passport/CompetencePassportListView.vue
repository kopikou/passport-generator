<template>
  <layout-h-c-f>
    <template #header>
      <div class="q-px-sm q-pb-sm">
        <div class="flex justify-between q-my-sm q-px-sm"
             style="display: grid; grid-template-columns: 1fr 1fr 220px auto auto; gap: 8px; align-items: center;">
          <q-select
            v-model="store.selectedYear"
            label="Год"
            :options="yearsList"
          />
        </div>
      </div>
    </template>
    <template #content>
      <div v-if="store.groupsList.length > 0"
           style="display: grid; grid-template-columns: 300px 1fr; overflow: hidden; height: 100%"
      >
        <!-- Левая панель со списком групп -->
        <q-list
          style="overflow-y: auto; height: 100%; box-shadow: 0 0 8px silver; z-index: 100"
          separator
        >
          <q-item
            v-for="group in store.groupsList"
            :key="group.plan_id"
            style="display: grid; gap: 8px;"
            clickable
            :active="store.currentPlanId === group.plan_id"
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
        <div v-if="store.currentPlanId" style="display: flex; flex-direction: column; height: 100%; padding: 20px;">
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
                  Выберите из уже загруженных учебных планов
                </div>
              </q-card-section>
              <q-card-actions>
                <q-btn color="primary" label="Выбрать" @click.stop="selectExistingPlan" />
              </q-card-actions>
            </q-card>
          </div>

          <!-- Отображение выбранного действия -->
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
              <div class="text-h6 q-mb-md">Существующие учебные планы</div>
              
              
              <!-- Список доступных файлов -->
              <div v-if="availablePlanFiles.length > 0">
                <div class="text-subtitle2 q-mb-sm">Доступные учебные планы:</div>
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
                  label="Выбрать этот план" 
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

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useCompetencePassportStore } from 'stores/competencePassportStore';
import { useRouter } from 'vue-router';
import { useQuasar } from 'quasar';
import _ from 'lodash';
import LayoutHCF from 'components/LayoutHCF.vue';
import dayjs from "dayjs";

const store = useCompetencePassportStore()
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

// Получение первого файла из массива plx_file
function getFirstPlxFile(plxFile) {
  if (!plxFile) return null;
  if (Array.isArray(plxFile) && plxFile.length > 0) {
    return plxFile[0];
  }
  return plxFile;
}

// Текущий файл учебного плана для выбранной группы
const currentGroupPlxFile = computed(() => {
  if (!store.currentPlanId) return null;
  const currentGroup = store.groupsList.find(group => group.plan_id === store.currentPlanId);
  return getFirstPlxFile(currentGroup?.plx_file);
});

// Доступные файлы учебных планов
const availablePlanFiles = computed(() => {
  if (!currentGroupPlxFile.value) return [];
  
  return [
    {
      name: getFileName(currentGroupPlxFile.value),
      url: currentGroupPlxFile.value
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


// Действия при выборе группы
async function selectGroup(planId) {
  store.currentPlanId = planId;
  selectedAction.value = '';
  selectedPlanFile.value = null;
  uploadedFile.value = null;
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

// Загрузка файла учебного плана
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

// Подтверждение выбора учебного плана
async function confirmPlanSelection() {
  if (!selectedPlanFile.value) {
    $q.notify({
      type: 'warning',
      message: 'Выберите учебный план'
    });
    return;
  }

  try {
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

// Загрузка данных при монтировании
onMounted(async () => {
  await store.fetchGroupsList()
})

// Обновление данных при изменении фильтров
watch([
  () => store.textFilter,
  () => store.groupTextFilter,
  () => store.statusFilter,
  () => store.myFilter,
  () => store.selectedYear
], _.debounce(async () => {
  await store.fetchGroupsList()
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