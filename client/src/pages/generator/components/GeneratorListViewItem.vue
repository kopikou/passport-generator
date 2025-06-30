<script setup lang="ts">
import {GeneratorListData} from "src/types";
import {computed, ref, watch} from "vue";
import GeneratorManageDialog from "pages/generator/components/dialogs/GeneratorManageDialog.vue";
import {useQuasar} from "quasar";
import _ from "lodash";
import {storeToRefs} from "pinia";
import useGeneratorViewStore from "stores/generatorViewStore";
import {useRouter} from "vue-router";
import {api} from "boot/axios";
import useMainStore from "stores/mainStore";

// const props = defineProps({
//   item: {
//     required: true,
//     type: Object as () => GeneratorListData
//   },
// })

const props = defineProps({
  items: {
    required: true
  },
});

const columns = [
  { name: 'discode', align: 'center', label: 'Код', field: 'discode', sortable: true },
  { name: 'discpl', align: 'center', label: 'Дисциплина', field: 'discpl', sortable: true },
  { name: 'person', align: 'center', label: 'Составитель', field: 'person', sortable: true },
  { name: 'kaf', align: 'center', label: 'Кафедра', field: 'kafcode', sortable: true },
  { name: 'rukprog', align: 'center', label: 'Согласован', field: 'rukprog', sortable: true },
  { name: 'zavkaf', align: 'center', label: 'Утвержден', field: 'zavkaf', sortable: true },
  { name: 'status_verbose', align: 'center', label: 'Статус', field: 'status_verbose', sortable: true },
  { name: 'control', align: 'center', label: 'Управление', field: 'type', sortable: false },
];

const generatorViewStore = useGeneratorViewStore();
const {
  cafData,
} = storeToRefs(generatorViewStore)

const mainStore = useMainStore();
const {
  FORCE_SCRIPT_NAME,
} = storeToRefs(mainStore);

const emit = defineEmits(['data-updated'])

const uploadRpdFile = ref();
const $q = useQuasar();
const router = useRouter();

// const canEdit = computed(() => {
//   const rules = ['person']
//   return props.item.type.some(q => rules.includes(q))
// })
//
// const canView = computed(() => {
//   const rules = ['rop', 'fac', 'zav']
//   return props.item.type.some(q => rules.includes(q))
// })
//
// const adminView = computed(() => {
//   const rules = ['view']
//   return props.item.type.some(q => rules.includes(q))
// })

function canEdit(item) {
  const rules = ['person']
  return item.type.some(q => rules.includes(q))
}

function canView(item) {
  const rules = ['rop', 'fac', 'zav']
  return item.type.some(q => rules.includes(q))
}

function adminView(item) {
  const rules = ['view']
  return item.type.some(q => rules.includes(q))
}

const cafDataById = computed(() => {
  return _.keyBy(cafData.value, 'value')
})

const fileName = computed((item) => {
  return decodeURI(item?.last_accepted_file_url || "").split('/').pop()
})

function openManageDialog(item) {
  $q.dialog({
    component: GeneratorManageDialog,
    componentProps: {
      id: item.id,
      data: item,
    }
  }).onOk(() => {
    emit('data-updated')
  })
}

function openUrl(url: string) {
  window.open(
    url,
    '_blank' // <- This is what makes it open in a new window.
  );
}

function fileFilter(files) {
  return files.filter(file => file.type === 'application/pdf')
}

watch(() => props.items, (item) => {
  uploadRpdFile.value = new File([], item?.last_accepted_file_url || '');
}, {
  immediate: true
})

async function onFileUploaded(item) {
  const loadingHelpers = $q.loading.show({
    group: 'third',
    message: 'Загружаю документ',
  })
  const formData = new FormData()
  formData.append('file', uploadRpdFile.value)

  let r = await api.post(`/api/generator/${item.id}/upload-rpd-program/`, formData)

  emit('data-updated')

  loadingHelpers()
}

function rowClassFn (row) {
  return `rpd-row status-${row.status}`;
}

</script>

<template>
      <q-table
        v-if="currentData !== null"
        :rows="items"
        :columns="columns"
        virtual-scroll
        style="overflow-y: auto; height: 100%;"
        wrap-cells
        row-key="discode"
        flat
        bordered
        separator="cell"
        :rows-per-page-options="[0]"
        :table-row-class-fn="rowClassFn"
        table-header-class="table-header"
      >

        <template #body-cell-kaf="props">
          <q-td>
            {{ cafDataById[props.row.kafcode]?.label }}
          </q-td>
        </template>

        <template #body-cell-rukprog="props">
          <q-td>
            <div :style="{color: props.row.user_confirmed_name === null ? 'grey' : ''}">
              <q-icon
                v-if="props.row.user_confirmed_name !== null"
                name="check"
                color="green"
                size="15px"
              >
              </q-icon>
              {{ props.row.rukprog }}
            </div>
          </q-td>
        </template>

        <template #body-cell-zavkaf="props">
          <q-td>
            <div :style="{color: props.row.user_accepted_name === null ? 'grey' : ''}">
              <q-icon
                v-if="props.row.user_accepted_name !== null"
                name="check"
                color="green"
                size="15px"
              >
              </q-icon>
              {{ props.row.zavkaf }}
            </div>
          </q-td>
        </template>

        <template #body-cell-control="props">
          <q-td>
              <div v-if="props.row.can_upload_file_directly">
                <q-file :label="'Загрузить программу'" outlined bottom-slots v-model="uploadRpdFile"
                        :filter="fileFilter"
                        accept="*.pdf, application/pdf"
                        style="width: 300px"
                        @update:model-value="onFileUploaded(props.row)"
                        max-files="1"
                        v-if="props.row.can_upload_file_directly"
                >

                  <template #file>
                    {{ fileName(props.row) }}
                  </template>

                  <template v-slot:after v-if="props.row.last_accepted_file_url">
                    <q-btn
                      icon="mdi-eye"
                      flat
                      dense
                      style="height: 100%"
                      v-show="props.row.last_accepted_file_url"
                      color="secondary"
                      @click="openUrl(props.row.last_accepted_file_url)"
                    />
                  </template>
                </q-file>
              </div>
              <div v-else>
                <q-btn v-if="canEdit(props.row)" dense flat color="primary" icon="mdi-pencil"
                       label="заполнить" @click="router.push(`/generator/${props.row.id}/main`)"/>
                <q-btn v-if="canView(props.row)" dense flat color="secondary" icon="mdi-briefcase-eye"
                       label="просмотр" @click="openManageDialog(props.row)"/>
                <q-btn v-if="adminView(props.row)" dense flat color="black" icon="mdi-download"
                       :href="`${FORCE_SCRIPT_NAME}/api/generator/${props.row.id}/get-rpd-report/`"
                       target="_blank"
                />
              </div>
          </q-td>
        </template>

      </q-table>
<!--  <div>{{ item.discode }}</div>-->
<!--  <div>{{ item.discpl }}</div>-->
<!--  <div>{{ item.person }}</div>-->
<!--  <div>{{ cafDataById[item.kafcode]?.label }}</div>-->
<!--  <div>{{ item.user_confirmed_name }}</div>-->
<!--  <div>{{ item.user_accepted_name }}</div>-->
<!--  <div>{{ item.status_verbose }}</div>-->
<!--  <div>-->
<!--    <template v-if="item.can_upload_file_directly">-->
<!--      <q-file :label="'Загрузить программу'" outlined bottom-slots v-model="uploadRpdFile"-->
<!--              :filter="fileFilter"-->
<!--              accept="*.pdf, application/pdf"-->
<!--              style="width: 300px"-->
<!--              @update:model-value="onFileUploaded"-->
<!--              max-files="1">-->

<!--        <template #file>-->
<!--          {{ fileName }}-->
<!--        </template>-->

<!--        <template v-slot:after v-if="item.last_accepted_file_url">-->
<!--          <q-btn-->
<!--            icon="mdi-eye"-->
<!--            flat-->
<!--            dense-->
<!--            style="height: 100%"-->
<!--            v-show="item.last_accepted_file_url"-->
<!--            color="secondary"-->
<!--            @click="openUrl(item.last_accepted_file_url)"-->
<!--          />-->
<!--        </template>-->
<!--      </q-file>-->
<!--    </template>-->
<!--    <template v-else>-->
<!--      <q-btn v-if="canEdit" dense flat color="primary" icon="mdi-pencil"-->
<!--             label="заполнить" @click="router.push(`/generator/${item.id}/main`)"/>-->
<!--      <q-btn v-if="canView" dense flat color="secondary" icon="mdi-briefcase-eye"-->
<!--             label="просмотр" @click="openManageDialog"/>-->
<!--      <q-btn v-if="adminView" dense flat color="black" icon="mdi-download"-->
<!--             :href="`${FORCE_SCRIPT_NAME}/api/generator/${item.id}/get-rpd-report/`"-->
<!--             target="_blank"-->
<!--      />-->
<!--    </template>-->
<!--  </div>-->
</template>

<style scoped>

</style>
