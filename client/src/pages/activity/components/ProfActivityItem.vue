<script setup lang="ts">

import QSelectFilterable from "components/QSelectFilterable.vue";
import {onBeforeMount, ref, watch, watchEffect} from "vue";
import {useQuasar} from "quasar";
import {useRouter} from "vue-router";
import useMainStore from "stores/mainStore";
import useProfActivityViewStore from "stores/profActivityViewStore";
import {storeToRefs} from "pinia";
import {api} from "boot/axios";
import _ from "lodash";


const $q = useQuasar()
const router = useRouter()

const props = defineProps({
  id: {
    require: true
  }
})

const mainStore = useMainStore();
const profActivityViewStore = useProfActivityViewStore();

const {
  areas_list,
  types_list,
  areaById,
  typeById,
  admissionDataById,
  currentItem,
} = storeToRefs(profActivityViewStore)

const {
  userId,
  mira_id,
} = storeToRefs(mainStore)

const area = ref()
const type_activity = ref()
const napr = ref()

const rowsAreas = ref([])
const columnsAreas = [
  {name: 'id', align: 'left', label: '', field: 'id'},
  {name: 'title', align: 'left', label: 'Наименование', field: 'title'},
  {name: 'actions', align: 'right', label: '', sortable: false},
]

const rowsTypes = ref([])
const columnsTypes = [
  {name: 'title', align: 'left', label: 'Наименование', field: 'title'},
  {name: 'actions', align: 'right', label: '', sortable: false},
]

async function addAreaItem() {
  const exists = rowsAreas.value.some(item => item.title === area.value.title);
  if (!exists) {
    await saveAreaData();
  }
  area.value = '';
}

async function saveAreaData() {
  const response = await api.post('/api/activity/save-areas-data/', {
    plan_mira_id: props.id,
    area: area.value.id,
  });
  if (response.status === 200) {
    await profActivityViewStore.getAdmissionDataForActivity()
    await updateRows()
    area.value = '';
  }

}

async function addTypeItem() {
  const exists = rowsTypes.value.some(item => item.title === type_activity.value.id);
  if (!exists) {
    await saveTypeData()
  }
  type_activity.value = ''
}

async function saveTypeData() {
  const response = await api.post('/api/activity/save-types-data/', {
    plan_mira_id: props.id,
    type: type_activity.value.id,
  });
  if (response.status === 200) {
    type_activity.value = '';
    await profActivityViewStore.getAdmissionDataForActivity()
    await updateRows()
  }
}

async function removeArea(data) {
  let r = await api.post(`/api/activity/${data}/remove-area-data/`)

  await profActivityViewStore.getAdmissionDataForActivity()
  await updateRows()
}

async function removeType(data) {
  let r = await api.post(`/api/activity/${data}/remove-type-data/`)

  await profActivityViewStore.getAdmissionDataForActivity()
  await updateRows()
}

function updateRows() {
  rowsAreas.value = []
  rowsTypes.value = []

  const data = _.get(admissionDataById.value, currentItem.value)
  _.map(data.areas, x => {
    rowsAreas.value.push({
      "id": x.id,
      "title": _.get(areaById.value, x.area_id).title
    })
  })
  _.map(data.types, x => {
    rowsTypes.value.push({
      "id": x.id,
      "title": _.get(typeById.value, x.type_id).title
    })
  })

}

watch(currentItem, () => {
  updateRows()
})


</script>

<template>
  <span class="admissionInfo" style="font-size: 1.5rem">{{admissionDataById[currentItem]?.species}}</span>
  <q-select-filterable
    filled
    outlined
    use-input
    input-debounce="500"
    emit-value
    map-options
    v-model="area"
    :options="areas_list"
    label="Область профессионнальной деятельности"
    option-label="title"
    options-value="id"
    clearable
    @update:model-value="addAreaItem"
  ></q-select-filterable>

  <q-table
    :rows="rowsAreas"
    :columns="columnsAreas"
    row-key="id"
    virtual-scroll
    wrap-cells
    no-data-label="Область профессиональной деятельности не выбрана"
    :rows-per-page-options="[0]"
  >
        <template #header-cell-id>
        </template>
        <template #body-cell-id>
        </template>
    <template v-slot:body-cell-actions="props">
      <q-td style="text-align: right">
        <q-btn
          flat
          color="negative"
          icon="delete"
          @click="removeArea(props.row.id)"
        />

      </q-td>
    </template>
  </q-table>
  <q-select-filterable
    class="q-mt-md"
    transition-show="jump-up"
    transition-hide="jump-up"
    filled
    outlined
    use-input
    input-debounce="500"
    emit-value
    map-options
    v-model="type_activity"
    :options="types_list"
    label="Вид профессионнальной деятельности"
    option-label="title"
    options-value="id"
    clearable
    @update:model-value="addTypeItem"
  >
  </q-select-filterable>

  <q-table
    :rows="rowsTypes"
    :columns="columnsTypes"
    row-key="id"
    wrap-cells
    virtual-scroll

    :rows-per-page-options="[0]"
    no-data-label="Вид профессиональной деятельности не выбран"
  >
    <template v-slot:body-cell-actions="props">
      <q-td style="text-align: right">
        <q-btn
          flat
          color="negative"
          icon="delete"
          @click="removeType(props.row.id)"
        />
      </q-td>
    </template>
  </q-table>
</template>

<style scoped lang="scss">
  .admissionInfo {
    background: linear-gradient(90deg, $purple-2, $orange-2);
  }
</style>
