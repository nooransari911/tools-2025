"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.CommonService = void 0;
const common_1 = require("@nestjs/common");
const axios_1 = require("axios");
const status_exception_1 = require("./exceptions/status.exception");
let CommonService = class CommonService {
    constructor() {
        this.hello_world_html_string = `
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Hello World</title>
                <style>
                    body {
                    background-color: black;
                    color: white;
                    font-family: 'Courier New', Courier, monospace;
                    }
                </style>
            </head>
            <body>
                <h1>Hello World</h1>
            </body>
        </html>
    `;
        this.src_db_base_url = "http://localhost:7000";
        this.dest_db_base_url = "http://localhost:8000";
        this.self_base_url = "http://localhost:3000";
        this.success_str = "successful";
        this.fail_not_found_str = "Not Found";
        this.fail_internal_str = "Internal Server Error";
        this.fail_badreq_str = "Bad Request";
        this.success_code = 200;
        this.fail_not_found_code = 404;
        this.fail_internal_code = 500;
        this.fail_badreq_code = 400;
    }
    async jets_france_from_route() {
        const response_france = await axios_1.default.get(`${this.self_base_url}/jet/france/`);
        return response_france.data;
    }
    async jets_china_from_db() {
        const response_china_1 = await axios_1.default.get(`${this.src_db_base_url}/1`);
        const response_china_2 = await axios_1.default.get(`${this.src_db_base_url}/2`);
        return [
            response_china_1.data,
            response_china_2.data
        ];
    }
    req_headers_string(req) {
        let req_headers_string = "<h1>Request Headers:</h1><p><ul>";
        let header;
        let var_header_string;
        for (const header in req.headers) {
            const headerval = req.headers[header];
            if (Array.isArray(headerval)) {
                var_header_string = headerval.join(', ');
            }
            else {
                var_header_string = headerval;
            }
            req_headers_string += `<li><strong>${header}</strong>: ${var_header_string}</li>`;
        }
        req_headers_string += "</ul></p>";
        return req_headers_string;
    }
    res_headers_string(res) {
        let res_headers_string = "<h1>Response Headers:</h1><p><ul>";
        let res_headers = res.getHeaders();
        let var_header_string;
        for (const header in res_headers) {
            const headerval = res_headers[header];
            if (Array.isArray(headerval)) {
                var_header_string = headerval.join(', ');
            }
            else {
                var_header_string = headerval;
            }
            res_headers_string += `<li><strong>${header}</strong>: ${var_header_string}</li>`;
        }
        res_headers_string += "</ul></p>";
        return res_headers_string;
    }
    async get_from_db_id(id) {
        try {
            const obj_promise = axios_1.default.get(`${this.src_db_base_url}/${id}`);
            const await_promise = await obj_promise;
            return await_promise.data;
        }
        catch (error) {
            throw new status_exception_1.InternalServerExc("Failed to get from db");
        }
    }
    async get_from_db_id_batch(ids) {
        try {
            const all_promises = ids.map(id => axios_1.default.get(`${this.src_db_base_url}/${id}`));
            const await_promises = await Promise.all(all_promises);
            const all_objs = await_promises.map(obj => obj.data);
            return all_objs;
        }
        catch (error) {
            throw new status_exception_1.InternalServerExc("Error fetching the objs");
        }
    }
    async get_from_dest_db_id_promise(id) {
        try {
            return axios_1.default.get(`${this.dest_db_base_url}/checkout/${id}`);
        }
        catch (error) {
            throw new status_exception_1.InternalServerExc("Failed to get from db");
        }
    }
    async post_to_db_obj(obj) {
        const a = {
            message: "hi",
            StatusCode: 200,
        };
        try {
            const obj_promise = await axios_1.default.post(`${this.dest_db_base_url}/checkout`, obj);
            return {
                message: this.success_str,
                StatusCode: this.success_code
            };
        }
        catch (error) {
            throw new status_exception_1.InternalServerExc("Failed to create/update object");
        }
    }
    async post_to_db_obj_batch(objs) {
        try {
            const all_promises = objs.map(obj => axios_1.default.post(`${this.dest_db_base_url}/checkout`, obj));
            const await_promises = await Promise.all(all_promises);
            const opress = {
                message: this.success_str,
                StatusCode: this.success_code
            };
            return opress;
        }
        catch (error) {
            throw new status_exception_1.InternalServerExc("Failed to add users batch");
        }
    }
    async delete_in_db(id) {
        try {
            const promise = await axios_1.default.delete(`${this.dest_db_base_url}/checkout/${id}`);
            return {
                message: this.success_str,
                StatusCode: this.success_code
            };
        }
        catch (error) {
            throw new status_exception_1.InternalServerExc("Failed to delete");
        }
    }
    async checkout_checkin(id) {
        try {
            await this.get_from_dest_db_id_promise(id);
            return await this.delete_in_db(id);
        }
        catch (error) {
            if (axios_1.default.isAxiosError(error) && error.response?.status === 404) {
                const objFromSource = await this.get_from_db_id(id);
                return await this.post_to_db_obj(objFromSource);
            }
            if (axios_1.default.isAxiosError(error)) {
                throw new status_exception_1.InternalServerExc(`Axios Error: ${error.message}`);
            }
            throw new status_exception_1.InternalServerExc("Failed to checkout/checkin");
        }
    }
};
exports.CommonService = CommonService;
exports.CommonService = CommonService = __decorate([
    (0, common_1.Injectable)()
], CommonService);
//# sourceMappingURL=common.service.js.map