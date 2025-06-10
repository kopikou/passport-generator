<script setup lang="ts">

import useUploadFileViewStore from "stores/uploadFileViewStore";
import {storeToRefs} from "pinia";
import FileUploader from "pages/upload/components/FileUploader.vue";
import _ from "lodash";
import {api} from "boot/axios";
import {useQuasar} from "quasar";
import {computed, ref} from "vue";
import useMainStore from "stores/mainStore";
import LayoutHCF from "components/LayoutHCF.vue";
import {PlanData} from "src/types";

const $q = useQuasar()


const mainStore = useMainStore();
const textFilter = ref("");
const {FORCE_SCRIPT_NAME} = storeToRefs(mainStore);


const uploadFileViewStore = useUploadFileViewStore();

const {
  admissionData,
  baseDocumentsById,
} = storeToRefs(uploadFileViewStore)

const {
  userId,
  mira_id,
} = storeToRefs(mainStore)


const admissionList = computed(() => {
  let txt = textFilter.value.toLowerCase();
  return _(admissionData.value).filter((x: any) => {
    return (!adms.value || adms.value.length == 0 || adms.value.includes(x.abbrprofile))
      && (!years.value || years.value.length == 0 || years.value.includes(x.startyear))
      && (!studyformFilter.value || studyformFilter.value.length == 0 || studyformFilter.value.includes(x.studyform))
      && (!studyprogFilter.value || studyprogFilter.value.length == 0 || studyprogFilter.value.includes(x.studyprog))
      && ((txt || "") == "" || x.abbrprofile.toLowerCase().includes(txt))
  }).sortBy(x => x['abbrprofile']).value()
})


const yearslist = computed(() => {
  return _.uniq(_.map(admissionData.value, (x) => x.startyear))
})

const admslist = computed(() => {
  return _.uniq(_.map(admissionData.value, (x) => x.abbrprofile))
})

const studyformList = computed(() => {
  return _.uniq(_.map(admissionData.value, (x) => x.studyform))
})

const studyprogList = computed(() => {
  return _.uniq(_.map(admissionData.value, (x) => x.studyprog))
})

const years = ref<string[]>([])
const adms = ref<string[]>([])
const studyformFilter = ref<string[]>([])
const studyprogFilter = ref<string[]>([])

function getFileUrl(item: PlanData, typeId: number) {
  let file = item.documents_files.find(x => x.type_id == typeId);
  if (file.url)
    window.open(`${FORCE_SCRIPT_NAME.value}` + file.url, "_blank")
  else if (file.file)
    window.open(`${FORCE_SCRIPT_NAME.value}` + file.file, "_blank")
}

function getFileId(item: PlanData, fileId) {
  let files = item.documents_files
  return _.filter(files, (x) => x.type_id == getFileType(item, fileId))[0]?.id
}

function getFileType(item: PlanData, fileId) {
  return _.filter(item.plan_documents, (x) => x.id == fileId)[0].new_type
}

function getRules(data, item) {
  if (data.can_upload == 't') return true
  const doc = baseDocumentsById.value[item.type_id]
  let rule = []
  if (data.admin) rule.push(0)
  if (data.cperson == mira_id.value) rule.push(1)

  return _.map(rule, x => {
    return doc.can_upload.includes(x)
  }).includes(true)

}

async function deleteFile(item: PlanData, typeId: number) {

  $q.dialog({
    title: 'Удаление файла',
    message: 'Вы точно хотите удалить выбранный файл?',
    ok: {
      label: 'Удалить',
      flat: true,
      color: 'red',
    },
    cancel: {
      label: 'Отмена',
      flat: true,
      color: 'green',
    },
    persistent: true
  }).onOk(async () => {
    $q.loading.show()
    let file = _.find(item.documents_files, (x) => x.type_id == typeId)
    let r = await api.delete(`/api/upload/${file.id}/`)
    item.documents_files = item.documents_files.filter(x => x!= file);
    $q.loading.hide()
  })
}

function checkFile(item: PlanData, typeId: number) {
  return item.documents_files.find(x => x.type_id == typeId)
  // let filesIds = _.map(item.documents_files, (x) => x.type_id)
  // let type = getFileType(item, fileId)
  // if (filesIds.includes(type)) return true
  // else return false
}

function checkUser(item: PlanData, typeId: number) {
  const data = item.documents_files.find(x => x.type_id == typeId)
  if (data) {
    return data.user_id == userId.value
  }
  return false
}

function sortDocuments(val) {
  return _.sortBy(val, x => _.get(baseDocumentsById.value, x.type_id, [])?.can_upload)
}

</script>

<template>
  <layout-h-c-f>
    <template #header>
      <div class="text-center text-h6 q-mb-md"></div>
      <div class="q-pa-md" style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px">
        <q-input v-model="textFilter" label="Направление"></q-input>
<!--        <q-select-->
<!--          class="col"-->
<!--          label="Направление"-->
<!--          use-chips-->
<!--          filled-->
<!--          clearable-->
<!--          :options="admslist"-->
<!--          v-model="adms"-->
<!--          multiple-->
<!--        />-->
        <q-select
          class="col"
          label="Год"
          use-chips
          filled
          clearable
          :options="yearslist"
          v-model="years"
          multiple
        />
         <q-select
          class="col"
          label="Форма"
          use-chips
          filled
          clearable
          :options="studyformList"
          v-model="studyformFilter"
          multiple
        />
         <q-select
          class="col"
          label="Уровень"
          use-chips
          filled
          clearable
          :options="studyprogList"
          v-model="studyprogFilter"
          multiple
        />
      </div>
    </template>
    <template #content>
      <q-list bordered>
        <q-expansion-item
          v-for="item in admissionData"
          expand-separator
          :caption="item.plan_name"
          :label="`${item.abbrprofile} ${item.startyear}`"
        >
          <q-card>
            <q-card-section class="card-body">
              <div class="card-header text-center">
                <div>
                  Наименование
                </div>
                <div>
                  Загруженные файлы
                </div>
              </div>
              <div class="card-container" v-for="i in sortDocuments(item.plan_documents)">
                <div>
                  {{ i.name }}
                </div>
                <div class="flex items-center" style="display: grid; grid-template-columns: 1fr auto">
                  <div v-if="!checkFile(item, i.type_id)">
                    <file-uploader :title="i.type__name" :file-id="i.id" :plan-id="item.plan_id" :disable="!getRules(item, i)"/>
                  </div>
                  <div v-else>
                    <q-field
                      outlined
                      stack-label
                      dense
                      bg-color="green-3"
                    >
                      <template v-slot:control>
                        {{ i.name }}
                      </template>
                      <template v-slot:append>
                        <q-btn
                          icon="mdi-eye"
                          flat
                          dense
                          style="height: 100%"
                          v-show="checkFile(item, i.type_id)"
                          color="secondary"
                          @click="getFileUrl(item, i.type_id)"
                        />
                      </template>
                    </q-field>
                  </div>
                  <q-btn v-show="getRules(item, i) && checkFile(item, i.type_id) && checkUser(item, i.type_id)" flat dense icon="mdi-delete" color="negative"
                         @click="deleteFile(item, i.type_id)" />
                </div>
              </div>
            </q-card-section>
          </q-card>
        </q-expansion-item>
      </q-list>
    </template>
  </layout-h-c-f>
</template>

<style scoped>

.card-body {

  .card-header {
    display: grid;
    grid-template-columns: 4fr 1fr;
  }

  .card-container {
    display: grid;
    grid-template-columns: 4fr 1fr;
    padding: 5px;
  }
}

</style>
