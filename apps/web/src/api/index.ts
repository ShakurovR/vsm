export const API_URL = process.env.REACT_APP_API_URL;

export async function fetchHandler<T>(
	input: RequestInfo | URL,
	init?: RequestInit | undefined,
	retry = 2,
): Promise<Api.Response<T>> {
	try {

		const response = await fetch((process.env.REACT_APP_API_URL || 'http://localhost:9000/') + input, init);

		const data = await response.json();

		if (retry === -1) {
			// const errorData = data as Api.Response.Error;

			return { isError: true, data };
		}

		if (response.ok) {
			return {
				isError: false,
				data,
			};
		}

		return {
			isError: true,
			data,
		};
	} catch (error) {
		const err = error as Error;

		console.error(error);

		return {
			isError: true,
			data: {
				detail: [
					{
						loc: ['unknown', 0],
						msg: err.message,
						type: 'unknown',
					},
				],
			},
		};
	}
}
