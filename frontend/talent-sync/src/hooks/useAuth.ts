import { CognitoIdentityClient } from "@aws-sdk/client-cognito-identity";
import {
  fromCognitoIdentityPool,
  CognitoIdentityCredentialProvider,
} from "@aws-sdk/credential-provider-cognito-identity";
import { AWSCredentials } from "../types/AWSCredentials";

const REGION = import.meta.env.VITE_AWS_REGION;
const IDENTITY_POOL_ID = import.meta.env.VITE_COGNITO_IDENTITY_POOL_ID;
const GOOGLE_CLIENT_ID = import.meta.env.VITE_OAUTH_CLIENT_ID;

// Return users id token from google and get temporary AWS credentials for API Gateways
export const useAuth = () => {
  const getTokensAndCreds = async (): Promise<{
    awsCredentials: AWSCredentials;
    accessToken: string;
  }> => {
    return new Promise((resolve, reject) => {
      if (!chrome?.identity || !chrome.identity.launchWebAuthFlow) {
        reject("Chrome identity API is not available.");
        return;
      }

      const redirectUri = chrome.identity.getRedirectURL();
      const nonce = Math.random()
        .toString(36)
        .substring(2);

      const authUrl = new URL("https://accounts.google.com/o/oauth2/v2/auth");
      authUrl.searchParams.set("client_id", GOOGLE_CLIENT_ID);
      authUrl.searchParams.set("response_type", "token id_token");
      authUrl.searchParams.set("redirect_uri", redirectUri);
      authUrl.searchParams.set("scope", "openid email profile");
      authUrl.searchParams.set("nonce", nonce);
      authUrl.searchParams.set("prompt", "consent");

      chrome.identity.launchWebAuthFlow(
        { url: authUrl.toString(), interactive: true },
        async (responseUrl) => {
          if (chrome.runtime.lastError || !responseUrl) {
            reject(
              chrome.runtime.lastError?.message ||
                "No response from WebAuthFlow"
            );
            return;
          }

          try {
            const urlFragment = responseUrl.split("#")[1]; // Everything after the #
            const params = new URLSearchParams(urlFragment);
            const idToken = params.get("id_token"); // To get temporary aws credentials
            const accessToken = params.get("access_token");

            if (!accessToken || !idToken) {
              reject("Missing tokens in response URL.");
              return;
            }

            const identityClient = new CognitoIdentityClient({
              region: REGION,
            });

            // Get temporary AWS credentials from AWS Cognito
            const credentialsProvider: CognitoIdentityCredentialProvider = fromCognitoIdentityPool(
              {
                client: identityClient,
                identityPoolId: IDENTITY_POOL_ID,
                logins: {
                  "accounts.google.com": idToken,
                },
              }
            );

            const tempCreds = await credentialsProvider();

            const awsCredentials: AWSCredentials = {
              accessKeyId: tempCreds.accessKeyId!,
              secretAccessKey: tempCreds.secretAccessKey!,
              sessionToken: tempCreds.sessionToken!,
              expiresAt: tempCreds.expiration!.getTime(),
            };

            resolve({
              awsCredentials: awsCredentials,
              accessToken: accessToken,
            });
          } catch (err) {
            reject("Failed to retrieve AWS credentials: " + err);
          }
        }
      );
    });
  };

  return { getTokensAndCreds };
};
